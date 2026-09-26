import math

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def softmax(xs):
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    total = sum(exps)
    return [x / total for x in exps]

# Three token vectors with four features each.
tokens = [
    [1.0, 0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0],
]

query = tokens[0]
keys = tokens

scores = [dot(query, key) / math.sqrt(len(query)) for key in keys]
weights = softmax(scores)

value = [sum(weights[i] * tokens[i][j] for i in range(len(tokens)))
         for j in range(len(tokens[0]))]

print("Attention scores:", [round(x, 4) for x in scores])
print("Attention weights:", [round(x, 4) for x in weights])
print("Context vector:", [round(x, 4) for x in value])
