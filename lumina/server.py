from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json, math, random

ROOT=Path(__file__).parent
MODEL=ROOT.parent/"09-lumina-core"/"model.json"

if not MODEL.exists():
    raise SystemExit("Missing model.json. Run: python3 09-lumina-core/train.py")

m=json.loads(MODEL.read_text(encoding="utf-8"))
chars=m["chars"]; stoi={c:i for i,c in enumerate(chars)}
W1=m["W1"]; b1=m["b1"]; W2=m["W2"]; b2=m["b2"]
H=len(b1); V=len(chars)

def softmax(z):
    mm=max(z)
    e=[math.exp(x-mm) for x in z]
    s=sum(e)
    return [x/s for x in e]

def generate(prompt, length=180):
    prompt="".join(c for c in prompt.lower() if c in stoi)
    if not prompt:
        prompt=chars[0]
    out=prompt
    cur=prompt[-1]
    for _ in range(length):
        x=stoi.get(cur,0)
        h=[math.tanh(W1[j][x]+b1[j]) for j in range(H)]
        logits=[sum(W2[i][j]*h[j] for j in range(H))+b2[i] for i in range(V)]
        cur=random.choices(chars,weights=softmax(logits),k=1)[0]
        out+=cur
    return out

class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, status=200):
        data=json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in {"/","/index.html"}:
            data=(ROOT/"index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        try:
            n=int(self.headers.get("Content-Length","0"))
            body=json.loads(self.rfile.read(n).decode())
            prompt=str(body.get("message",""))
            answer=generate(prompt)
            self.send_json({"reply":answer})
        except Exception as e:
            self.send_json({"error":str(e)},500)

    def log_message(self, fmt, *args):
        print("[server]", fmt % args)

print("Lumina-1 website: http://127.0.0.1:8000")
HTTPServer(("127.0.0.1",8000),Handler).serve_forever()
