def shape(m):
    if not m: return (0,0)
    w=len(m[0])
    if any(len(r)!=w for r in m): raise ValueError("Unequal row lengths.")
    return (len(m),w)

def transpose(m):
    r,c=shape(m)
    return [[m[i][j] for i in range(r)] for j in range(c)]

def add(a,b):
    if shape(a)!=shape(b): raise ValueError("Shapes must match.")
    return [[x+y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]

def multiply(a,b):
    ar,ac=shape(a); br,bc=shape(b)
    if ac!=br: raise ValueError("Inner dimensions must match.")
    return [[sum(a[i][k]*b[k][j] for k in range(ac)) for j in range(bc)] for i in range(ar)]

def show(m):
    for row in m: print(" ",row)

if __name__=="__main__":
    A=[[1,2,3],[4,5,6]]
    B=[[7,8],[9,10],[11,12]]
    print("Lumina-1 — Matrix Experiment")
    print("\nA:"); show(A)
    print("\nB:"); show(B)
    print("\nA transposed:"); show(transpose(A))
    print("\nA x B:"); show(multiply(A,B))
    print("\nNeural networks repeatedly transform vectors using matrices of weights.")
