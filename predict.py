import json
from pathlib import Path

from network import TinyNetwork


MODEL_FILE = Path(__file__).with_name("weights.json")


def load_network():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "weights.json does not exist. Run train.py first."
        )

    with MODEL_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    network = TinyNetwork()
    network.w1 = data["w1"]
    network.b1 = data["b1"]
    network.w2 = data["w2"]
    network.b2 = data["b2"]

    return network


def main():
    network = load_network()

    examples = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ]

    print("Lumina-1 — Trained Predictions")
    print()

    for inputs in examples:
        prediction = network.predict(inputs)

        print(
            f"input={inputs} "
            f"prediction={prediction:.4f}"
        )


if __name__ == "__main__":
    main()
