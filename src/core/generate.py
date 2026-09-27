import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model.json"


def load_model():
    if not MODEL.exists():
        raise SystemExit(
             "Missing model.json. Run: python -m src.core.train
        )

    return json.loads(MODEL.read_text(encoding="utf-8"))


def softmax(logits):
    if not logits:
        return []

    m = max(logits)
    e_logits = [math.exp(x - m) for x in logits]
    total = sum(e_logits)

    if total <= 0:
        return [1.0 / len(e_logits)] * len(e_logits)

    return [x / total for x in e_logits]


def generate(prompt, length=250, model=None):

    m = model if model is not None else load_model()

    chars = m["chars"]
    stoi = {c: i for i, c in enumerate(chars)}

    W1 = m["W1"]
    b1 = m["b1"]
    W2 = m["W2"]
    b2 = m["b2"]

    H = len(b1)
    V = len(chars)

    prompt = "".join(
        c for c in prompt.lower()
        if c in stoi
    )

    if not prompt:
        prompt = chars[0]

    out = prompt

    for _ in range(length):
        x = stoi.get(out[-1], 0)

        h = [
            math.tanh(W1[j][x] + b1[j])
            for j in range(H)
        ]

        logits = [
            sum(W2[i][j] * h[j] for j in range(H)) + b2[i]
            for i in range(V)
        ]

        weights = softmax(logits)

        cur = random.choices(
            chars,
            weights=weights,
            k=1
        )[0]

        out += cur

    return out


if __name__ == "__main__":
    start = input("Prompt [lumina]: ").lower() or "lumina"
    n = int(input("Characters [250]: ") or "250")

    print(
        "\n--- Lumina-1 ---\n"
        + generate(start, n)
    )
