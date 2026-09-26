import random

def normalize(values):
    total=sum(values)
    if total<=0: raise ValueError("Total must be positive.")
    return [v/total for v in values]

def sample_index(probabilities):
    r=random.random(); total=0
    for i,p in enumerate(probabilities):
        total+=p
        if r<total: return i
    return len(probabilities)-1

if __name__=="__main__":
    words=["the","cat","runs"]
    probabilities=normalize([2,1,1])
    print("Lumina-1 — Probability Experiment")
    for word,p in zip(words,probabilities):
        print(f"{word:>5}: {p:.2%}")
    print("\n10 samples:")
    for _ in range(10):
        print(words[sample_index(probabilities)],end=" ")
    print("\n\nA language model eventually produces probabilities for possible next tokens.")
