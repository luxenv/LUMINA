from pathlib import Path
from datetime import datetime
import json

FILE=Path(__file__).parent/"memory.json"

def load():
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else []

def save(items):
    FILE.write_text(json.dumps(items,indent=2),encoding="utf-8")

def remember(text):
    items=load()
    items.append({"text":text,"created":datetime.now().isoformat(timespec="seconds")})
    save(items[-100:])

while True:
    x=input("1 remember / 2 show / 3 exit: ").strip()
    if x=="1":
        remember(input("Memory: ")); print("Saved.")
    elif x=="2":
        for item in load()[-10:]: print("-",item["text"])
    elif x=="3": break
