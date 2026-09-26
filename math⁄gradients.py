def function(x):
    return (x-3)**2

def derivative(x):
    return 2*(x-3)

def numerical_derivative(f,x,epsilon=1e-6):
    return (f(x+epsilon)-f(x-epsilon))/(2*epsilon)

def gradient_descent(x,learning_rate,steps):
    for step in range(steps):
        g=derivative(x)
        x=x-learning_rate*g
        print(f"step={step+1:02d} x={x:.6f} loss={function(x):.6f} gradient={g:.6f}")
    return x

if __name__=="__main__":
    x=7.0
    print("Lumina-1 — Gradient Experiment")
    print("f(x)=(x-3)^2")
    print("Exact derivative:",derivative(x))
    print("Numerical derivative:",numerical_derivative(function,x))
    print("\nGradient descent:")
    final=gradient_descent(x,0.1,10)
    print("\nFinal x:",final)
