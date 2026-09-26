# Milestone 9 — Lumina-1 Core

This milestone assembles a tiny trainable character language model.

To keep it practical on low-end hardware, the core uses a compact feed-forward
architecture rather than a large Transformer. The previous milestones explain
the pieces that modern Transformers use.

The model learns:
    context -> hidden representation -> next-character probabilities

Run:
    python3 09-lumina-core/train.py

Then:
    python3 09-lumina-core/generate.py

The generated `model.json` is the local Lumina-1 model used by later
milestones.
