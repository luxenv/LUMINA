class CharacterTokenizer:
    def __init__(self, text):
        self.chars = sorted(set(text))
        self.stoi = {c: i for i, c in enumerate(self.chars)}
        self.itos = {i: c for c, i in self.stoi.items()}

    def encode(self, text):
        return [self.stoi[c] for c in text]

    def decode(self, ids):
        return "".join(self.itos[i] for i in ids)


if __name__ == "__main__":
    sample = "Lumina-1 learns."
    tok = CharacterTokenizer(sample)
    ids = tok.encode(sample)
    print("Text:   ", sample)
    print("IDs:    ", ids)
    print("Decoded:", tok.decode(ids))
    print("Vocabulary:", tok.chars)
