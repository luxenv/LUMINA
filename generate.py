import json, math, random
from pathlib import Path

ROOT=Path(__file__).parent
m=json.loads((ROOT/"model.json").read_text(encoding="utf-8"))
chars=m["chars"]; stoi={c:i for i,c in enumerate(chars)}
W1=m["W1"]; b1=m["b1"]; W2=m["W2"]; b2=m["b2"]
H=len(b1); V=len(chars)

def softmax(z):
    mm=max(z); e=[math.exp(x-mm) for x in z]; s=sum(e)
    return [x/s for x in e]

def predict(ch):
    x=stoi.get(ch, 0)
    h=[math.tanh(W1[j][x]+b1[j]) for j in range(H)]
    logits=[sum(W2[i][j]*h[j] for j in range(H))+b2[i] for i in range(V)]
    return softmax(logits)

start=input("Prompt [lumina]: ").lower() or "lumina"
start="".join(c for c in start if c in stoi) or chars[0]
n=int(input("Characters [250]: ") or "250")

out=start
cur=start[-1]
for _ in range(n):
    p=predict(cur)
    cur=random.choices(chars,weights=p,k=1)[0]
    out+=cur

print("\n--- Lumina-1 ---\n"+out)
