# LUMINA

> A solo experimental language model project built from scratch with Python made by luxenv.

**LUMINA** is an ongoing experiment in understanding how language models work by building one from the ground up.

Rather than relying on an existing LLM framework or pretrained model, LUMINA's early versions focus on implementing the fundamentals myself: dataset processing, model training, text generation, memory, knowledge storage, feedback, tools, and a simple web interface.

LUMINA is still an experimental project. The current **v1 architecture is intentionally small and acts as a proof of concept**, with future versions planned to introduce more capable contextual models and eventually Transformer-based architectures.

---

## Features

### Experimental Language Model

LUMINA v1 contains a very small neural language model trained from scratch.

The current model:

* Uses a character-level vocabulary
* Predicts the next character
* Uses a small feed-forward neural network
* Trains entirely from a local dataset
* Saves its learned weights to `model.json`
* Generates text locally without requiring an external AI API

The v1 model is intentionally minimal. Its purpose is to demonstrate the fundamental language-model training and generation pipeline rather than compete with modern LLMs.

### Chat Interface

LUMINA includes a lightweight web interface that allows users to interact with the model through a browser.

The server provides endpoints for:

* Chat
* Feedback
* Knowledge management
* Knowledge search
* Statistics

### Memory

LUMINA includes a basic conversation-memory system.

The server can retain recent conversation turns and use them when constructing the prompt sent to the model.

### Knowledge Base

LUMINA includes a simple local knowledge system that can:

* Add information
* Search stored information
* Log user queries
* Provide additional context to the chatbot

### Tool Router

A basic tool-routing system is included as part of the architecture.

This is intended to provide a foundation for allowing LUMINA to determine when external or internal tools should be used.

### Feedback System

LUMINA includes a feedback component designed to collect information about interactions.

This provides a foundation for eventually using user feedback to improve the system.

### Lightweight Web Server

The project uses Python's standard library for its server rather than depending on a large web framework.

This keeps the prototype lightweight and makes the architecture easier to understand and experiment with.

---

# Architecture

The current project is organized roughly like this:

```text
LUMINA/
├── src/
│   ├── core/
│   │   ├── dataset.txt
│   │   ├── generate.py
│   │   ├── model.json
│   │   └── train.py
│   │
│   ├── model/
│   │   ├── neural/
│   │   └── transformer/
│   │
│   ├── features/
│   │   ├── feedback/
│   │   ├── knowledge/
│   │   ├── memory/
│   │   └── tools/
│   │
│   └── server/
│       └── app.py
│
├── web/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── scripts/
├── deploy/
└── docs/
```

The project is separated into several layers:

```text
Dataset
   ↓
Training
   ↓
Language Model
   ↓
Generation
   ↓
Memory / Knowledge / Tools
   ↓
Server
   ↓
Web Interface
```

This separation is intended to make it possible to replace the experimental v1 model with a more capable architecture without having to rebuild the entire application.

---

# LUMINA v1

## Version 1 — Experimental Prototype

LUMINA v1 is the first major proof of concept.

The goal of v1 was not to create a powerful chatbot.

The goal was to answer a much simpler question:

> **Can I build a tiny language model myself and connect it to an actual chatbot application?**

The answer was yes.

### v1 Model

The initial model uses:

* Character-level tokenization
* A vocabulary generated directly from the dataset
* A small hidden layer
* `tanh` activation
* Softmax output
* Next-character prediction
* Stochastic text generation
* JSON-based model storage

The model contains only around **1,600 trainable parameters**, making it extremely small compared with modern language models.

### v1 Training

The training process:

1. Loads `dataset.txt`
2. Builds a character vocabulary
3. Converts characters into integer IDs
4. Creates a small neural network
5. Trains the network to predict the next character
6. Saves the resulting weights to `model.json`

### v1 Generation

During generation, LUMINA takes a starting prompt and repeatedly predicts the next character.

For example:

```text
Prompt:
hello

       ↓

Language Model

       ↓

Predicted characters

       ↓

Generated text
```

Because the v1 model has extremely limited context, generated text can be repetitive, fragmented, or nonsensical.

This is an expected limitation of the prototype rather than the intended final behavior of LUMINA.

---

# 📜 Version Log

## LUMINA v1.0.0 — Initial Prototype

### Added

* Initial character-level language model
* Custom tokenizer
* Dataset-based training
* Neural next-character prediction
* JSON model serialization
* Local text generation
* Basic conversation memory
* Local knowledge base
* Feedback collection
* Tool routing foundation
* Python HTTP server
* Browser-based chat interface
* Basic deployment configuration
* Project documentation

### Model

```text
Architecture: Small feed-forward neural network
Tokenizer: Character-level
Training objective: Next-character prediction
Hidden size: 24
Model size: ~1.6K parameters
Dependencies: Python standard library
```

### Current Status

**Experimental / Prototype**

LUMINA v1 successfully demonstrates the complete pipeline from dataset → training → model → generation → web application.

However, the v1 language model is not capable of producing consistently coherent natural language.

---

# Known Limitations

LUMINA v1 is intentionally limited.

### Model limitations

* Extremely small parameter count
* Character-level representation
* Very limited context
* No embeddings
* No attention mechanism
* No Transformer blocks
* No semantic representation of words
* Limited ability to maintain context
* Limited language understanding

### Training limitations

* Small training dataset
* Simple optimization procedure
* No batching
* No validation dataset
* No sophisticated learning-rate scheduling
* No checkpoint system

### Generation limitations

The model may produce:

```text
fragmented words
repetition
incorrect spelling
random character sequences
```

These behaviors are expected from such a small experimental architecture.

---

# 📌 Current Status

**Current version: LUMINA v1.0.0**

**Stage: Experimental prototype**

LUMINA v1 is functional, but its language model is intentionally primitive.

The current priority is improving the underlying model architecture while keeping the surrounding application infrastructure intact.

---

## License

See [`LICENSE`](LICENSE) for license information.

---

## Acknowledgment

LUMINA is a personal project created as an experiment in understanding and building language-model technology from the ground up.
