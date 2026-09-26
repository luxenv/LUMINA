import random
import math

random.seed(1)

vocab = ["a", "b", "c", "d", "e"]
dimension = 8

table = {
    token: [random.uniform(-0.5, 0.5) for _ in range(dimension)]
    for token in vocab
}

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb)

for token, vector in table.items():
    print(token, ["%.3f" % x for x in vector])

print("\nSimilarity examples:")
print("a vs b:", round(cosine(table["a"], table["b"]), 4))
print("a vs a:", round(cosine(table["a"], table["a"]), 4))
