from pathlib import Path
import re,sys

doc=Path(__file__).parent/"knowledge.txt"
chunks=[x.strip() for x in re.split(r"\n\s*\n",doc.read_text(encoding="utf-8")) if x.strip()]

def words(s): return set(re.findall(r"[a-z0-9]+",s.lower()))

def retrieve(query,k=3):
    q=words(query)
    ranked=sorted(((len(q & words(c)),c) for c in chunks),reverse=True)
    return [c for score,c in ranked[:k] if score]

if __name__=="__main__":
    q=" ".join(sys.argv[1:]) or input("Question: ")
    for i,c in enumerate(retrieve(q),1): print(f"\n[{i}] {c}")
