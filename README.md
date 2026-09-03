# 🔗 DoLearn

A small Python library for building causal graphs, sampling from them, and simulating interventions.

## Features

- 🕸️ **Causal graph structure** — `CausalGraph` extends NetworkX's `DiGraph`, tracking parent relationships between nodes automatically as edges are added
- 🎲 **Sampling** — draw values from the graph's current state, respecting the causal structure
- ✋ **Interventions** — do-calculus style interventions (the "do" in DoLearn) that override a node's value and propagate downstream effects
- 📊 **Visualization** — built on `matplotlib` for plotting graphs
- 📚 **Docs site** — an MkDocs + mkdocstrings site (`mkdocs.yml`) with an API reference and a Jupyter notebook quickstart

## Installation

```bash
git clone <this repo>
cd do-learn
pip install -r requirements.txt
```

## Usage

```python
from do_learn.causal_graph import CausalGraph

g = CausalGraph(nodes=["A", "B"], edges=[("A", "B")])
values = g.sample()
```

To build and serve the docs locally:

```bash
mkdocs serve
```

## Built with

- [NetworkX](https://networkx.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [MkDocs](https://www.mkdocs.org/) + [mkdocstrings](https://mkdocstrings.github.io/) for docs

## Status

🔧 `requirements.txt` was missing `matplotlib` (imported directly by `causal_graph.py`), so `pip install -r requirements.txt` succeeded but importing `do_learn` failed with `ModuleNotFoundError`. Fixed by adding `matplotlib==3.11.1` to `requirements.txt`. Verified working as of 2026-09-03: `pip install -r requirements.txt` then `from do_learn.causal_graph import CausalGraph; CausalGraph(nodes=["A","B"], edges=[("A","B")]).sample()` runs cleanly. Still no packaging (`setup.py`/`pyproject.toml`) or test suite — used by importing the `do_learn` folder directly rather than installing as a package.
