from pathlib import Path
import json
f=Path(__file__).parent/"feedback.jsonl"
if not f.exists(): raise SystemExit("No feedback yet.")
for line in f.read_text(encoding="utf-8").splitlines():
    x=json.loads(line)
    print("\nPrompt:",x["prompt"],"\nResponse:",x["response"],"\nRating:",x["rating"],"\nNote:",x["note"])
