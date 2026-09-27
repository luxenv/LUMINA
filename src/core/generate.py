import json
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "model.json"


def load_model():

    if not MODEL.exists():
        raise SystemExit(
            "Missing model.json. Run: python -m src.core.train"
        )

    return json.loads(
        MODEL.read_text(
            encoding="utf-8"
        )
    )


def softmax(logits):

    if not logits:
        return []

    maximum = max(logits)

    exp_logits = [
        math.exp(x - maximum)
        for x in logits
    ]

    total = sum(exp_logits)

    if total <= 0:
        return [
            1.0 / len(exp_logits)
            for _ in exp_logits
        ]

    return [
        x / total
        for x in exp_logits
    ]


def generate(
    prompt,
    length=250,
    model=None
):

    model = (
        model
        if model is not None
        else load_model()
    )

    chars = model["chars"]

    stoi = {
        char: index
        for index, char in enumerate(chars)
    }

    W1 = model["W1"]
    b1 = model["b1"]
    W2 = model["W2"]
    b2 = model["b2"]

    hidden_size = len(b1)
    vocab_size = len(chars)

    # Keep only characters known by the model.
    cleaned_prompt = "".join(
        char
        for char in prompt.lower()
        if char in stoi
    )

    if not cleaned_prompt:
        cleaned_prompt = chars[0]

    # Use the final character of the prompt
    # as the starting input to the character model.
    current_char = cleaned_prompt[-1]

    generated = []

    for _ in range(length):

        x = stoi.get(
            current_char,
            0
        )

        hidden = [
            math.tanh(
                W1[j][x] + b1[j]
            )
            for j in range(hidden_size)
        ]

        logits = [
            sum(
                W2[i][j] * hidden[j]
                for j in range(hidden_size)
            ) + b2[i]
            for i in range(vocab_size)
        ]

        probabilities = softmax(logits)

        next_char = random.choices(
            chars,
            weights=probabilities,
            k=1
        )[0]

        generated.append(next_char)

        current_char = next_char

    return "".join(generated)


if __name__ == "__main__":

    start = (
        input("Prompt [lumina]: ").lower()
        or "lumina"
    )

    length = int(
        input("Characters [250]: ")
        or "250"
    )

    print("\n--- Lumina-1 ---")

    print(
        generate(
            start,
            length
        )
    )
