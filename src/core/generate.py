import json, math, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model.json"


def load_model():
    if not MODEL.exists():
        raise SystemExit("Missing model.json. Run: python -m src.core.train")
    return json.loads(MODEL.read_text(encoding="utf-8"))


def generate(prompt, length=250):
    m = load_model()
    chars = m["chars"]
    stoi = {c: i for i, c in enumerate(chars)}
    W1, b1, W2, b2 = m["W1"], m["b1"], m["W2"], m["b2"]
    H = len(b1)
    prompt = "".join(c for c in prompt.lower() if c in stoi) or chars[0]
    out, cur = prompt, prompt[-1]
    for _ in range(length):
        x = stoi.get(cur, 0)
        h = [math.tanh(W1[j][x] + b1[j]) for j in range(H)]
        logits = [sum(W2[i][j] * h[j] for j in range(H)) + b2[i] for i in range(len(chars))]
        mm = max(logits)
        weights = [math.exp(x - mm) for x in logits]
        cur = random.choices(chars, weights=weights, k=1)[0]
        out += cur
    return out


if __name__ == "__main__":
    start = input("Prompt [lumina]: ").lower() or "lumina"
    n = int(input("Characters [250]: ") or "250")
    print("\n--- Lumina-1 ---\n" + generate(start, n))
