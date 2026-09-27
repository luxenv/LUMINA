import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from threading import Lock

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
sys.path.insert(0, str(ROOT))

from src.core.generate import generate  # noqa: E402
from src.features.memory.context import ConversationMemory  # noqa: E402
from src.features.feedback.feedback import FeedbackCollector  # noqa: E402
from src.features.knowledge.kb import KnowledgeBase  # noqa: E402
from src.features.tools.router import ToolRouter  # noqa: E402

_cached_model = None
_model_lock = Lock()

kb = KnowledgeBase()
tool_router = ToolRouter(kb=kb)
feedback = FeedbackCollector()


def get_cached_model():
    """Lazy-load and cache model in memory."""
    global _cached_model
    if _cached_model is None:
        with _model_lock:
            if _cached_model is None:
                model_path = ROOT / "src" / "core" / "model.json"
                with open(model_path) as f:
                    _cached_model = json.load(f)
    return _cached_model


class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, status=200):
        data = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        routes = {
            "/": "index.html",
            "/index.html": "index.html",
            "/style.css": "style.css",
            "/script.js": "script.js",
        }
        
        if path == "/api/stats":
            self.send_json({
                "status": "online",
                "feedback_stats": feedback.get_statistics(),
                "model_cache": "active"
            })
            return
        
        name = routes.get(path)
        if not name:
            self.send_error(404)
            return
        
        file = WEB / name
        if not file.exists():
            self.send_error(404, f"Missing web asset: {name}")
            return
        
        data = file.read_bytes()
        if name.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif name.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        else:
            content_type = "text/javascript; charset=utf-8"
        
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        
        if path == "/api/chat":
            self._handle_chat()
        elif path == "/api/feedback":
            self._handle_feedback()
        elif path == "/api/knowledge/add":
            self._handle_add_knowledge()
        elif path == "/api/knowledge/search":
            self._handle_search_knowledge()
        else:
            self.send_error(404)
    
    def _handle_chat(self):
        
        try:
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size).decode())
            
            prompt = str(body.get("message", ""))
            session_id = body.get("session_id", "default")
            use_tools = body.get("use_tools", True)
            
            if not prompt.strip():
                self.send_json({"error": "Empty message"}, 400)
                return
            
            memory = ConversationMemory(session_id)
            
            tool_result = None
            tool_used = False
            tool_name = None

            if use_tools:
                tool_router.set_memory(memory)

                tool_used, tool_result = (
                    tool_router.route_and_execute(prompt)
                )

                if tool_used:
                    tool_name, _ = (
                        tool_router.detect_tool_request(prompt)
                    )

            if tool_used:
                reply = str(tool_result)

            else:
                context_str = memory.get_formatted_context(
                    max_turns=3
                )

                augmented_prompt = (
                    f"{context_str}{prompt}"
                )

                model = get_cached_model()

                reply = generate(
                    augmented_prompt,
                    180,
                    model=model
                )
            
            memory.save_turn(prompt, reply, metadata={
                "tool_used": tool_result is not None,
                "tool_result": tool_result
            })
            
            kb.log_query(prompt, reply, used_kb=tool_result is not None)
            
            self.send_json({
                "reply": reply,
                "session_id": session_id,
                "tool_used": tool_result is not None
            })
        
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)
    
    def _handle_feedback(self):
        
        try:
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size).decode())
            
            prompt = body.get("prompt", "")
            generated = body.get("generated_text", "")
            rating = body.get("rating", 3)
            notes = body.get("notes", "")
            
            feedback.log_feedback(prompt, generated, rating, notes)
            
            self.send_json({
                "status": "feedback_recorded",
                "avg_rating": feedback.get_statistics()["avg_rating"]
            })
        
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)
    
    def _handle_add_knowledge(self):
        
        try:
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size).decode())
            
            key = body.get("key", "")
            value = body.get("value", "")
            category = body.get("category", "general")
            
            if not key or not value:
                self.send_json({"error": "key and value required"}, 400)
                return
            
            kb.add_fact(key, value, category)
            self.send_json({"status": "fact_added", "key": key})
        
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)
    
    def _handle_search_knowledge(self):
        
        try:
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size).decode())
            
            query = body.get("query", "")
            if not query:
                self.send_json({"error": "query required"}, 400)
                return
            
            results = kb.search_facts(query)
            self.send_json({
                "query": query,
                "results": [{"key": r[0], "value": r[1], "category": r[2]} for r in results]
            })
        
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)
    
    def log_message(self, fmt, *args):
        print("[server]", fmt % args)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "8000"))
    print(f"Lumina-1 website: http://127.0.0.1:{port}")
    print(f"Knowledge base: {kb.db_path}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
