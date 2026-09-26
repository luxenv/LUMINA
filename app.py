from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import json,math,random,re,os
from datetime import datetime

ROOT=Path(__file__).parent; PROJECT=ROOT.parent
MODEL=PROJECT/"09-lumina-core"/"model.json"
KNOWLEDGE=PROJECT/"13-offline-knowledge"/"knowledge.txt"
MEMORY=ROOT/"memory.json"

if not MODEL.exists(): raise SystemExit("Run 09-lumina-core/train.py first.")
m=json.loads(MODEL.read_text(encoding="utf-8"))
chars=m["chars"]; stoi={c:i for i,c in enumerate(chars)}
W1=m["W1"]; b1=m["b1"]; W2=m["W2"]; b2=m["b2"]; H=len(b1); V=len(chars)

def softmax(z):
    q=max(z); e=[math.exp(x-q) for x in z]; s=sum(e); return [x/s for x in e]

def generate(prompt,n=180):
    clean="".join(c for c in prompt.lower() if c in stoi) or chars[0]
    out=clean; cur=clean[-1]
    for _ in range(n):
        x=stoi.get(cur,0)
        h=[math.tanh(W1[j][x]+b1[j]) for j in range(H)]
        logits=[sum(W2[i][j]*h[j] for j in range(H))+b2[i] for i in range(V)]
        cur=random.choices(chars,weights=softmax(logits),k=1)[0]; out+=cur
    return out

def calc(expr):
    import ast,operator as op
    ops={ast.Add:op.add,ast.Sub:op.sub,ast.Mult:op.mul,ast.Div:op.truediv,
         ast.Pow:op.pow,ast.Mod:op.mod,ast.USub:op.neg}
    def v(n):
        if isinstance(n,ast.Expression): return v(n.body)
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n,ast.UnaryOp) and type(n.op) in ops:return ops[type(n.op)](v(n.operand))
        if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](v(n.left),v(n.right))
        raise ValueError()
    return v(ast.parse(expr,mode="eval"))

def retrieve(q):
    if not KNOWLEDGE.exists(): return []
    chunks=[x.strip() for x in re.split(r"\n\s*\n",KNOWLEDGE.read_text(encoding="utf-8")) if x.strip()]
    words=lambda s:set(re.findall(r"[a-z0-9]+",s.lower()))
    qw=words(q)
    return [c for _,c in sorted(((len(qw&words(c)),c) for c in chunks),reverse=True)[:2] if _]

def remember(text):
    items=json.loads(MEMORY.read_text(encoding="utf-8")) if MEMORY.exists() else []
    items.append({"text":text,"created":datetime.now().isoformat(timespec="seconds")})
    MEMORY.write_text(json.dumps(items[-100:],indent=2),encoding="utf-8")

def answer(msg):
    low=msg.lower().strip()
    if low.startswith(("calculate ","calc ")):
        try:return "Calculator result: "+str(calc(msg.split(" ",1)[1]))
        except:pass
    if low.startswith("remember "):
        remember(msg[9:]); return "Saved that to local memory."
    context=retrieve(msg)
    return generate(msg+" "+" ".join(context),220) if context else generate(msg,220)

class Handler(BaseHTTPRequestHandler):
    def send_json(self,x,status=200):
        data=json.dumps(x,ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Content-Length",str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path in ("/","/index.html"):
            data=(ROOT/"index.html").read_bytes(); self.send_response(200)
            self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(data)))
            self.end_headers(); self.wfile.write(data)
        else:self.send_error(404)
    def do_POST(self):
        if self.path!="/api/chat":self.send_error(404);return
        try:
            n=int(self.headers.get("Content-Length","0")); body=json.loads(self.rfile.read(n).decode())
            self.send_json({"reply":answer(str(body.get("message","")))})
        except Exception as e:self.send_json({"error":str(e)},500)
    def log_message(self,*a): pass

port=int(os.environ.get("PORT","8000"))
print("Lumina-1 listening on",port)
HTTPServer(("0.0.0.0",port),Handler).serve_forever()
