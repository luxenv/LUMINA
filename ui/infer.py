import json, math, random
from pathlib import Path

MODEL = Path(__file__).parent.parent / "09-lumina-core" / "model.json"
if not MODEL.exists():
    raise SystemExit("Train Milestone 9 first.")

m=json.loads(MODEL.read_text(encoding="utf-8"))
chars=m["chars"]; stoi={c:i for i,c in enumerate(chars)}
W1=m["W1"]; b1=m["b1"]; W2=m["W2"]; b2=m["b2"]
H=len(b1); V=len(chars)

def softmax(z):
    mm=max(z)
    e=[math.exp(x-mm) for x in z]
    s=sum(e)
    return [x/s for x in e]

def next_char(ch):
    x=stoi.get(ch, 0)
    h=[math.tanh(W1[j][x]+b1[j]) for j in range(H)]
    logits=[sum(W2[i][j]*h[j] for j in range(H))+b2[i] for i in range(V)]
    return random.choices(chars,weights=softmax(logits),k=1)[0]

def generate(prompt, length=200):
    prompt="".join(c for c in prompt.lower() if c in stoi)
    if not prompt:
        prompt=chars[0]
    out=prompt
    cur=prompt[-1]
    for _ in range(length):
        cur=next_char(cur)
        out+=cur
    return out

while True:
    prompt=input("\nYou: ")
    if prompt.lower() in {"exit","quit"}:
        break
    print("Lumina-1:", generate(prompt, 180))
