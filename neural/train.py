import json
import math
from pathlib import Path

from network import TinyNetwork, sigmoid_derivative


DATA = [
    ([0.0, 0.0], 0.0),
    ([0.0, 1.0], 1.0),
    ([1.0, 0.0], 1.0),
    ([1.0, 1.0], 0.0),
]

MODEL_FILE = Path(__file__).with_name("weights.json")


def train(network, data, learning_rate=1.0, epochs=10000):
    for epoch in range(epochs):
        total_loss = 0.0

        for inputs, target in data:
            hidden, output = network.forward(inputs)

            # Mean squared error for this one example.
            error = output - target
            total_loss += error * error

            # Output layer gradient.
            d_output = (
                2.0
                * error
                * sigmoid_derivative(output)
            )

            old_w2 = network.w2[:]

            # Output weights and bias.
            for index in range(2):
                gradient = d_output * hidden[index]
                network.w2[index] -= learning_rate * gradient

            network.b2 -= learning_rate * d_output

            # Hidden layer gradients.
            for hidden_index in range(2):
                d_hidden = (
                    d_output
                    * old_w2[hidden_index]
                    * sigmoid_derivative(hidden[hidden_index])
                )

                for input_index in range(2):
                    gradient = d_hidden * inputs[input_index]
                    network.w1[input_index][hidden_index] -= (
                        learning_rate * gradient
                    )

                network.b1[hidden_index] -= (
                    learning_rate * d_hidden
                )

        if epoch % 1000 == 0 or epoch == epochs - 1:
            average_loss = total_loss / len(data)
            print(
                f"epoch={epoch:5d} "
                f"loss={average_loss:.6f}"
            )


def save_network(network):
    data = {
        "w1": network.w1,
        "b1": network.b1,
        "w2": network.w2,
        "b2": network.b2,
    }

    with MODEL_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def main():
    network = TinyNetwork()

    print("Lumina-1 — Training")
    print("Learning the XOR pattern...")
    print()

    train(network, DATA)

    save_network(network)

    print()
    print(f"Saved learned parameters to: {MODEL_FILE}")


if __name__ == "__main__":
    main()
