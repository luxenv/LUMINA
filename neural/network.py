import math


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(output):
    return output * (1.0 - output)


class TinyNetwork:
    def __init__(self):
        # 2 inputs -> 2 hidden neurons -> 1 output neuron.
        self.w1 = [
            [0.5, -0.5],
            [0.5, -0.5],
        ]
        self.b1 = [0.0, 0.0]

        self.w2 = [0.5, -0.5]
        self.b2 = 0.0

    def forward(self, inputs):
        hidden = []

        for neuron_index in range(2):
            total = self.b1[neuron_index]

            for input_index in range(2):
                total += (
                    inputs[input_index]
                    * self.w1[input_index][neuron_index]
                )

            hidden.append(sigmoid(total))

        output_total = self.b2
        for index in range(2):
            output_total += hidden[index] * self.w2[index]

        output = sigmoid(output_total)

        return hidden, output

    def predict(self, inputs):
        _, output = self.forward(inputs)
        return output


def main():
    network = TinyNetwork()

    examples = [
        ([0.0, 0.0], 0.0),
        ([0.0, 1.0], 1.0),
        ([1.0, 0.0], 1.0),
        ([1.0, 1.0], 0.0),
    ]

    print("Lumina-1 — Tiny Neural Network")
    print("Before training:")

    for inputs, target in examples:
        prediction = network.predict(inputs)
        print(
            f"input={inputs} "
            f"target={target:.0f} "
            f"prediction={prediction:.4f}"
        )

    print()
    print("This network is intentionally untrained.")
    print("Training happens in train.py.")


if __name__ == "__main__":
    main()
