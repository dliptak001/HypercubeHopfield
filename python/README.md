# HypercubeHopfield

**HypercubeHopfield** — modern Hopfield associative memory on a Boolean
hypercube. Neurons sit on the vertices of a dim-dimensional cube
(`N = 2^dim`). Patterns are stored **explicitly** and retrieved by
**softmax attention** over a sparse neighborhood — not collapsed into a
Hebbian weight matrix, and not full all-to-all modern-Hopfield attention
either.

**A topology you don't store.** Connectivity is the mask table of the
Hamming ball — one XOR per neighbor, no adjacency list, at any size.
Each vertex attends only inside that ball; cost scales with connections,
not with the full cube.

---

<p align="center">
  <strong>HypercubeAI ecosystem</strong><br/>
</p>

<p align="center">
  <a href="https://github.com/dliptak001/HypercubeESN"><strong>HypercubeESN</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dliptak001/HypercubeCNN"><strong>HypercubeCNN</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dliptak001/HypercubeHopfield"><strong>HypercubeHopfield</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dliptak001/HypercubeWTF"><strong>HypercubeWTF</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dliptak001/HypercubeEtalon"><strong>HypercubeEtalon</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dliptak001/HypercubeCascade"><strong>HypercubeCascade</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dliptak001/HypercubeLCN"><strong>HypercubeLCN</strong></a>
</p>

<p align="center">
  📄 Foundational paper:
  <a href="https://github.com/dliptak001/HypercubeHopfield/blob/main/docs/Boolean_hypercubes_as_a_neural_substrate.pdf"><em>Boolean Hypercubes as a Neural Substrate</em></a>
  (D.&nbsp;C.&nbsp;Liptak, 2026)
</p>

HypercubeHopfield is an experiment in the **HypercubeAI** project — our quest to
systematically re-implement classical neural architectures on a Boolean
hypercube topology instead of Euclidean grids or random graphs. The central
thesis is “topology-native intelligence”: the hypercube’s algebraic structure
(vertex-transitive symmetry, Hamming geometry, bitwise addressing) can serve
as a first-class computational substrate.

- **A topology you don’t store** — the graph is specified: connectivity is
  implicit in the vertex indices; with a seed and a few config scalars the whole
  reservoir reconstructs mathematically.
- **Perfect homogeneity** — every vertex has the same degree and the same local
  world, so local dynamics mean the same thing everywhere — no structural
  favorites baked in by a random graph.
- **Cheap navigation** — each neighbor is a few bit operations on the vertex
  index, not a pointer chase through a stored edge list, so walks stay
  arithmetic and cache-friendly.
- **Topology-native pairing** — the readout consumes the reservoir’s output with
  zero geometric distortion, and the learned kernels exploit the same locality
  that generated the dynamics. The data never leaves the hypercube it was born
  on.

Each product in the family is a different architecture on that same foundation.

---

## Installation

```bash
pip install hypercube-hopfield
```

Pre-built wheels for **Python 3.10–3.13** on Windows, Linux, and macOS.
NumPy is the only runtime dependency.

Build from source (C++23 + CMake): see the [Python SDK guide](https://github.com/dliptak001/HypercubeHopfield/blob/main/docs/Python_SDK.md).

## Quick Start

```python
import numpy as np
import hypercube_hopfield as hh

# 256 neurons (dim=8, N=2^8)
net = hh.HopfieldNetwork(dim=8, seed=42)

patterns = np.random.randn(10, net.num_vertices).astype(np.float32)
net.store_patterns(patterns)

cue = patterns[0] + np.random.randn(net.num_vertices).astype(np.float32) * 0.3
result = net.recall(cue)
print(f"Converged: {result.converged}, steps: {result.steps}")
# result.state is the cleaned recall; input cue is not modified
```

## Features

- **Explicit pattern storage** — modern Hopfield retrieval without a Hebbian weight matrix
- **Sparse Hamming-ball attention** — `reach` and `neighbor_fraction` control connectivity and cost
- **Two update modes** — Sync (default, deterministic) and Async (guaranteed energy descent)
- **Pickle / `save` / `load`** — persist config and all stored patterns
- **NumPy integration** — automatic float32 conversion; `recall` does not mutate the cue

## Documentation

- [Python SDK Reference](https://github.com/dliptak001/HypercubeHopfield/blob/main/docs/Python_SDK.md) — full API, persistence, errors
- [Project README](https://github.com/dliptak001/HypercubeHopfield) — architecture framing, C++ quick start, build
- [HopfieldNetwork architecture](https://github.com/dliptak001/HypercubeHopfield/blob/main/docs/HopfieldNetwork.md) — connectivity, energy, parameters
