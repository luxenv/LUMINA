def tokenize(text):
    return text.split()

if __name__=="__main__":
    text=input("Enter text: ")
    for index, token in enumerate(tokenize(text)):
        print(f"{index}: {token}")
