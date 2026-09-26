import json, random
from pathlib import Path

ROOT = Path(__file__).parent
model = json.loads((ROOT / "model.json").read_text(encoding="utf-8"))
chars = model["chars"]
probs = model["probs"]
stoi = {c: i for i, c in enumerate(chars)}

current = input("Starting character (Enter for 'l'): ").lower() or "l"
if current not in stoi:
    current = chars[0]

length = int(input("Characters to generate [200]: ") or "200")
out = current

for _ in range(length - 1):
    row = probs[stoi[current]]
    current = random.choices(chars, weights=row, k=1)[0]
    out += current

print("\n--- Lumina-1 ---")
print(out)
