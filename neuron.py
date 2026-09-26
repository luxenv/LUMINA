import math


def sigmoid(x):
    # Squashes any number into a value between 0 and 1.
    return 1.0 / (1.0 + math.exp(-x))


def neuron(inputs, weights, bias):
    if len(inputs) != len(weights):
        raise ValueError("Inputs and weights must have the same length.")

    weighted_sum = sum(x * w for x, w in zip(inputs, weights)) + bias
    return sigmoid(weighted_sum)


def main():
    inputs = [1.0, 0.5]
    weights = [0.8, -0.4]
    bias = 0.2

    output = neuron(inputs, weights, bias)

    print("Lumina-1 — Single Neuron")
    print("Inputs: ", inputs)
    print("Weights:", weights)
    print("Bias:   ", bias)
    print(f"Output:  {output:.6f}")
    print()
    print("A neuron multiplies inputs by weights, adds a bias,")
    print("then passes the result through an activation function.")


if __name__ == "__main__":
    main()
