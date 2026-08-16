# HypercubeHopfield

[![Build wheels](https://github.com/dliptak001/HypercubeHopfield/actions/workflows/wheels.yml/badge.svg)](https://github.com/dliptak001/HypercubeHopfield/actions/workflows/wheels.yml)
[![PyPI](https://img.shields.io/pypi/v/hypercube-hopfield)](https://pypi.org/project/hypercube-hopfield/)
[![Python](https://img.shields.io/pypi/pyversions/hypercube-hopfield)](https://pypi.org/project/hypercube-hopfield/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![C++23](https://img.shields.io/badge/C%2B%2B-23-blue.svg)](https://en.cppreference.com/w/cpp/23)

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

## Quick Start

### Python

```bash
pip install hypercube-hopfield
```

```python
import numpy as np
import hypercube_hopfield as hh

net = hh.HopfieldNetwork(dim=8, seed=42)

patterns = np.random.randn(10, net.num_vertices).astype(np.float32)
net.store_patterns(patterns)

cue = patterns[0] + np.random.randn(net.num_vertices).astype(np.float32) * 0.5
result = net.recall(cue)
print(f"Converged: {result.converged}, sweeps: {result.steps}")
```

Pre-built wheels for Python 3.10–3.13 on Windows, Linux, and macOS.
Full API: [docs/Python_SDK.md](docs/Python_SDK.md).

### C++

```cpp
#include "HopfieldNetwork.h"

auto net = CreateHopfieldNetwork(/*dim=*/8, /*seed=*/42);
net->StorePattern(pattern);                  // span<const float>, size N = 256
auto [steps, converged] = net->Recall(cue);  // modifies cue in place
```

CMake FetchContent or `find_package`. Guide: [docs/CPP_SDK.md](docs/CPP_SDK.md).

---

## How this differs

**Classical Hopfield** folds patterns into a weight matrix (Hebbian) and
converges under a quadratic energy. Cross-talk in that matrix is the
bottleneck.

**Modern Hopfield** (Ramsauer et al., 2021) keeps patterns explicit and
retrieves with a log-sum-exp energy — mathematically the same softmax
attention as a transformer. The usual formulation is fully connected over
the state.

**HypercubeHopfield** keeps the modern energy and explicit storage, but
wires each vertex only to its **Hamming ball**. Neighbor lookup is XOR
against a shared mask table (sorted closest-first, optionally truncated).
Cost is **O(M × connections)** per vertex, on a cube you can grow to
DIM 4–16 (16 … 65,536 neurons).

Sync updates (default) are double-buffered, deterministic, and threaded.
Async updates guarantee monotonic energy descent. Both stop when no
vertex moves more than `tolerance`.

Deep dive: [docs/HopfieldNetwork.md](docs/HopfieldNetwork.md).

---

## Documentation

| Document | Covers |
|----------|--------|
| [docs/CPP_SDK.md](docs/CPP_SDK.md) | C++ SDK: FetchContent, find_package, API reference |
| [docs/Python_SDK.md](docs/Python_SDK.md) | Python SDK: installation, API reference, persistence |
| [docs/HopfieldNetwork.md](docs/HopfieldNetwork.md) | Connectivity, update rule, energy, parameters |
| [examples/AutoAssociativeDemo.md](examples/AutoAssociativeDemo.md) | Sensor fault recovery — noise and dropout |
| [examples/HeteroAssociativeDemo.md](examples/HeteroAssociativeDemo.md) | Diagnostic lookup — input→output association |

---

## Building from Source

**Requirements:** C++23 compiler (GCC 13+, Clang 17+, MSVC 2022+), CMake 4.1+.

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/HypercubeHopfield
```

No external dependencies beyond the C++ standard library. MinGW, GCC/Clang,
and MSVC are detected automatically. The main binary runs the diagnostics
suite; example targets build from `examples/`.

---

## Layout

```
HypercubeHopfield/
  HopfieldNetwork.h/cpp   Public core API
  main.cpp                Diagnostics entry point
  diagnostics/            Noise, energy, overlap, and related probes
  examples/               Auto- and heteroassociative demos
  python/                 PyPI package (hypercube-hopfield)
  docs/                   Architecture + C++/Python SDK
  cmake/                  Install / package config
```
