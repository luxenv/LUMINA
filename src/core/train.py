import json, math, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
text = (ROOT / "dataset.txt").read_text(encoding="utf-8").lower()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}

# A very small neural next-character model.
V = len(chars)
H = 24
random.seed(7)
W1 = [[random.uniform(-0.15, 0.15) for _ in range(V)] for _ in range(H)]
b1 = [0.0] * H
W2 = [[random.uniform(-0.15, 0.15) for _ in range(H)] for _ in range(V)]
b2 = [0.0] * V


def softmax(z):
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


def forward(x):
    h = [math.tanh(W1[j][x] + b1[j]) for j in range(H)]
    logits = [sum(W2[i][j] * h[j] for j in range(H)) + b2[i] for i in range(V)]
    return h, softmax(logits)


lr = 0.08
epochs = 35

for epoch in range(epochs):
    total = 0.0
    order = list(range(len(text) - 1))
    random.shuffle(order)
    for pos in order:
        x = stoi[text[pos]]
        target = stoi[text[pos + 1]]
        h, p = forward(x)
        total += -math.log(max(p[target], 1e-12))
        dz = p[:]
        dz[target] -= 1.0
        oldW2 = [row[:] for row in W2]
        for i in range(V):
            for j in range(H):
                W2[i][j] -= lr * dz[i] * h[j]
            b2[i] -= lr * dz[i]
        dh = [sum(oldW2[i][j] * dz[i] for i in range(V)) for j in range(H)]
        for j in range(H):
            dh[j] *= 1 - h[j] * h[j]
            W1[j][x] -= lr * dh[j]
            b1[j] -= lr * dh[j]
    if epoch % 5 == 0 or epoch == epochs - 1:
        print(f"epoch {epoch + 1:02d}/{epochs} loss={total / (len(text) - 1):.4f}")

model = {"chars": chars, "W1": W1, "b1": b1, "W2": W2, "b2": b2}
output = ROOT / "model.json"
output.write_text(json.dumps(model), encoding="utf-8")
print("Saved:", output)
