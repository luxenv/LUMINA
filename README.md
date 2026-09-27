# LUMINA

<p align="center">
  <strong>A lightweight, local AI experiment built from scratch.</strong>
</p>

<p align="center">
  <a href="https://github.com/luxenv/LUMINA/releases">
    <img src="https://img.shields.io/badge/version-1.3.0-blue.svg" alt="Version 1.3.0">
  </a>
  <img src="https://img.shields.io/badge/python-3.x-yellow.svg" alt="Python 3">
  <img src="https://img.shields.io/badge/status-experimental-orange.svg" alt="Experimental">
</p>

## Overview

LUMINA is a local AI project combining a small character-level neural network with application-level tools.

Current features include:

* Character-level text generation
* Tool routing
* Calculator
* Time tool
* Local web interface
* Modular application architecture

> LUMINA is an experimental project. Some functionality is currently rule-based and the neural model is intentionally small.

## Quick Start

### 1. Clone

```bash
git clone https://github.com/luxenv/LUMINA.git
cd LUMINA
```

### 2. Run

```bash
python -m src.server.app
```

Then open:

```text
http://127.0.0.1:8000
```

### 3. Train the model

If you want to train the model yourself:

```bash
python -m src.core.train
```

The trained model is saved to:

```text
src/core/model.json
```

## Direct Generation

You can run the neural generator without the web server:

```bash
python -m src.core.generate
```

## Project Structure

```text
src/
├── core/       # Model, training, and generation
├── features/   # Tools and additional features
└── server/     # Local application server

web/            # Web interface
docs/           # Documentation
scripts/        # Utility scripts
```

## Roadmap

**v1.3.0** — Tool integration and application architecture

**v1.4.0** — Memory system

**Future** — Improved natural-language understanding and tool interaction

## License

See [LICENSE](LICENSE) for license information.

<p align="center">
  <sub>LUMINA is built as an ongoing learning and experimentation project.</sub>
</p>
