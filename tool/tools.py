import ast, operator as op

OPS={ast.Add:op.add,ast.Sub:op.sub,ast.Mult:op.mul,
     ast.Div:op.truediv,ast.Pow:op.pow,ast.Mod:op.mod,ast.USub:op.neg}

def calculate(expression):
    def visit(n):
        if isinstance(n,ast.Expression): return visit(n.body)
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n,ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](visit(n.operand))
        if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](visit(n.left),visit(n.right))
        raise ValueError("Unsupported expression")
    return visit(ast.parse(expression,mode="eval"))

if __name__=="__main__":
    while True:
        x=input("Calculate (or exit): ").strip()
        if x.lower()=="exit": break
        try: print(calculate(x))
        except Exception as e: print("Error:",e)
