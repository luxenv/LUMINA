def tokenize(text):
    # A deliberately simple first tokenizer. Real LLM tokenizers come later.
    return text.split()

if __name__=="__main__":
    text=input("Enter text: ")
    for index, token in enumerate(tokenize(text)):
        print(f"{index}: {token}")
