from pathlib import Path
from datetime import datetime
import json

FILE=Path(__file__).parent/"feedback.jsonl"
while True:
    prompt=input("\nPrompt (or exit): ")
    if prompt.lower()=="exit": break
    response=input("Response: ")
    rating=input("Rating 1-5: ")
    note=input("Note: ")
    item={"time":datetime.now().isoformat(timespec="seconds"),
          "prompt":prompt,"response":response,"rating":rating,"note":note}
    with FILE.open("a",encoding="utf-8") as f: f.write(json.dumps(item,ensure_ascii=False)+"\n")
    print("Saved for review; model unchanged.")
