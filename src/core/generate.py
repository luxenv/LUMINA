import json, math, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model.json"


def load_model():
    if not MODEL.exists():
        raise SystemExit("Missing model.json. Run: python -m src.core.train")
    return json.loads(MODEL.read_text(encoding="utf-8"))


def softmax(logits):
    """Properly normalized softmax for probability distribution."""
    if not logits:
        return []
    m = max(logits)
    e_logits = [math.exp(x - m) for x in logits]
    s = sum(e_logits)
    return [x / s for x in e_logits] if s > 0 else [1.0 / len(e_logits)] * len(e_logits)


def generate(prompt, length=250, context_size=32):
    """Generate text with proper context window and normalized probabilities.
    
    Args:
        prompt: Starting text
        length: Number of characters to generate
        context_size: Number of previous chars to use as context (default 32)
    """
    m = load_model()
    chars = m["chars"]
    stoi = {c: i for i, c in enumerate(chars)}
    W1, b1, W2, b2 = m["W1"], m["b1"], m["W2"], m["b2"]
    H = len(b1)
    V = len(chars)
    
    # Sanitize and pad prompt
    prompt = "".join(c for c in prompt.lower() if c in stoi) or chars[0]
    context = prompt.rjust(context_size, chars[0])[-context_size:]
    
    out = prompt
    for _ in range(length):
        # Use context window: average character indices for context-aware prediction
        context_indices = [stoi.get(c, 0) for c in context]
        # Simple context aggregation: use position-weighted sum
        x = sum((i + 1) * idx for i, idx in enumerate(context_indices)) % V
        
        # Forward pass
        h = [math.tanh(W1[j][x] + b1[j]) for j in range(H)]
        logits = [sum(W2[i][j] * h[j] for j in range(H)) + b2[i] for i in range(V)]
        
        # Normalized softmax
        weights = softmax(logits)
        cur = random.choices(chars, weights=weights, k=1)[0]
        out += cur
        
        # Slide context window
        context = (context + cur)[-context_size:]
    
    return out


if __name__ == "__main__":
    start = input("Prompt [lumina]: ").lower() or "lumina"
    n = int(input("Characters [250]: ") or "250")
    print("\n--- Lumina-1 ---\n" + generate(start, n))
