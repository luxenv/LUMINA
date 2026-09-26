import math

def softmax(xs):
    m = max(xs)
    e = [math.exp(x-m) for x in xs]
    s = sum(e)
    return [v/s for v in e]

def matvec(matrix, vector):
    return [sum(a*b for a,b in zip(row, vector)) for row in matrix]

def attention(x):
    # Tiny identity-like Q, K, V projections.
    q = x
    k = x
    v = x
    scores = [sum(a*b for a,b in zip(q, k)) / math.sqrt(len(q))]
    weights = softmax(scores)
    return [weights[0] * z for z in v]

def transformer_block(sequence):
    # Residual connection around the attention output.
    result = []
    for token in sequence:
        a = attention(token)
        result.append([x+y for x,y in zip(token, a)])
    return result

sequence = [
    [0.2, 0.1, 0.4, 0.3],
    [0.8, 0.2, 0.1, 0.0],
    [0.1, 0.7, 0.2, 0.1],
]

print("Input:")
for row in sequence:
    print(row)

print("\nOutput:")
for row in transformer_block(sequence):
    print([round(x, 4) for x in row])
