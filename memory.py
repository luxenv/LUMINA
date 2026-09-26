from pathlib import Path

MEMORY_FILE=Path(__file__).with_name("memory.txt")

def save_memory(text):
    with MEMORY_FILE.open("a",encoding="utf-8") as file:
        file.write(text.strip()+"\n")

def read_memory():
    if not MEMORY_FILE.exists(): return []
    with MEMORY_FILE.open("r",encoding="utf-8") as file:
        return [line.rstrip("\n") for line in file]

if __name__=="__main__":
    print("Lumina-1 — Simple File Memory")
    print("1. Save memory")
    print("2. Read memory")
    choice=input("Choose: ").strip()
    if choice=="1":
        save_memory(input("Memory to save: "))
        print("Memory saved.")
    elif choice=="2":
        memories=read_memory()
        print("\n".join(f"{i}. {m}" for i,m in enumerate(memories,1)) or "No memories yet.")
    else:
        print("Unknown option.")
