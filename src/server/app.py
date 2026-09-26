import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
sys.path.insert(0, str(ROOT))

from src.core.generate import generate  # noqa: E402


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
        files = {"/": "index.html", "/index.html": "index.html", "/style.css": "style.css", "/script.js": "script.js"}
        name = files.get(path)
        if not name:
            self.send_error(404)
            return
        file = WEB / name
        if not file.exists():
            self.send_error(404, f"Missing web asset: {name}")
            return
        data = file.read_bytes()
        content_type = "text/html; charset=utf-8" if name.endswith(".html") else "text/css; charset=utf-8" if name.endswith(".css") else "text/javascript; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size).decode())
            self.send_json({"reply": generate(str(body.get("message", "")), 180)})
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)

    def log_message(self, fmt, *args):
        print("[server]", fmt % args)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "8000"))
    print(f"Lumina-1 website: http://127.0.0.1:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
