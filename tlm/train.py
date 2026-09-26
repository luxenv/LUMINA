import json
from pathlib import Path

ROOT = Path(__file__).parent
text = (ROOT / "dataset.txt").read_text(encoding="utf-8").lower()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}

counts = [[0 for _ in chars] for _ in chars]
for a, b in zip(text, text[1:]):
    counts[stoi[a]][stoi[b]] += 1

probs = []
for row in counts:
    total = sum(row)
    probs.append([(x + 1) / (total + len(chars)) for x in row])

model = {"chars": chars, "probs": probs}
(ROOT / "model.json").write_text(json.dumps(model), encoding="utf-8")
print("Saved model.json")
print("Vocabulary size:", len(chars))
