# Milestone 3 — Neural Network

This milestone builds Lumina-1's first actual learning system.

The network is intentionally tiny and uses only Python's standard library. The goal is understanding, not speed.

## What this teaches

- Inputs and outputs
- Weights and biases
- Activation functions
- Forward propagation
- Loss
- Gradients
- Backpropagation
- Gradient descent
- Training data
- Predictions

## Run it

From the Lumina-1 project directory:

```bash
python3 03-neural-network/neuron.py
python3 03-neural-network/network.py
python3 03-neural-network/train.py
python3 03-neural-network/predict.py
```

## The learning loop

Lumina-1's tiny network follows this basic process:

```text
input
  ↓
weights + bias
  ↓
prediction
  ↓
loss
  ↓
gradient
  ↓
update weights
  ↓
better prediction
```

This is the foundation that later becomes much more complicated in a language model.

## Files

### `neuron.py`
A single neuron implemented from scratch.

### `network.py`
A small two-layer neural network with sigmoid activation.

### `train.py`
Trains the network on a tiny XOR dataset.

### `predict.py`
Loads the trained parameters and uses them to make predictions.

### `weights.json`
Created by `train.py` after training. It contains the learned parameters.

## Important limitation

This is NOT a language model yet. It learns a simple numerical pattern.

The purpose is to understand the mechanism that eventually allows a neural network to learn language.

## Milestone 3 goal

By the end of this milestone, you should understand:

1. What a neuron does.
2. Why weights and biases exist.
3. What an activation function does.
4. What a loss function measures.
5. What a gradient tells us.
6. How backpropagation calculates parameter gradients.
7. How gradient descent changes parameters.
8. How repeated training can reduce error.

## Next milestone

**Milestone 4 — Tiny Language Model**

We will move from learning numerical patterns to predicting text.
