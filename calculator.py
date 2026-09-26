def calculate(a, operator, b):
    if operator == "+": return a + b
    if operator == "-": return a - b
    if operator == "*": return a * b
    if operator == "/":
        if b == 0: raise ValueError("Cannot divide by zero.")
        return a / b
    raise ValueError("Unknown operator.")

def main():
    print("Lumina-1 — Python Calculator")
    print("Operators: +  -  *  /")
    print("Type 'q' to quit.")
    while True:
        first=input("First number: ").strip()
        if first.lower()=="q": break
        try:
            a=float(first); op=input("Operator: ").strip(); b=float(input("Second number: "))
            print(f"Result: {calculate(a,op,b)}")
        except ValueError as error:
            print(f"Error: {error}")
        print()

if __name__=="__main__":
    main()
