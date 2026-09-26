import math

def add(a,b):
    if len(a)!=len(b): raise ValueError("Vectors must have the same length.")
    return [x+y for x,y in zip(a,b)]

def subtract(a,b):
    if len(a)!=len(b): raise ValueError("Vectors must have the same length.")
    return [x-y for x,y in zip(a,b)]

def scale(v,n): return [x*n for x in v]

def dot(a,b):
    if len(a)!=len(b): raise ValueError("Vectors must have the same length.")
    return sum(x*y for x,y in zip(a,b))

def magnitude(v): return math.sqrt(sum(x*x for x in v))

def cosine_similarity(a,b):
    d=magnitude(a)*magnitude(b)
    if d==0: raise ValueError("Zero vector.")
    return dot(a,b)/d

if __name__=="__main__":
    a=[1,2,3]; b=[4,5,6]
    print("Lumina-1 — Vector Experiment")
    print("A =",a); print("B =",b)
    print("A+B =",add(a,b))
    print("A-B =",subtract(a,b))
    print("2A =",scale(a,2))
    print("A dot B =",dot(a,b))
    print("|A| =",round(magnitude(a),4))
    print("cos(A,B) =",round(cosine_similarity(a,b),4))
