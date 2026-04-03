# HypercubeHopfield Python SDK

Python bindings for modern Hopfield associative memory on Boolean hypercube graphs.

## Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [The dim parameter](#the-dim-parameter)
  - [Enums](#enums)
  - [HopfieldNetwork](#hopfieldnetwork)
- [Input Data Layout](#input-data-layout)
- [Error Handling](#error-handling)
- [Model Persistence](#model-persistence)
- [Limitations](#limitations)
- [Dependencies](#dependencies)

## Installation

### From PyPI (recommended)

Pre-built wheels are available for Python 3.10-3.13 on Windows (x64),
Linux (x86_64, aarch64), and macOS (x86_64, arm64):

```bash
pip install hypercube-hopfield
```

### From source

Requirements: Python 3.10+, a C++23 compiler (GCC 13+, Clang 17+, MSVC 2022+), CMake 3.20+.

```bash
git clone https://github.com/dliptak001/HypercubeHopfield.git
cd HypercubeHopfield/python
pip install .
```

On Windows with MinGW, install build dependencies and set compiler environment
variables before building:

```powershell
pip install scikit-build-core pybind11 numpy
$env:PATH = "C:\path\to\mingw\bin;" + $env:PATH
$env:CMAKE_GENERATOR = "Ninja"
$env:CMAKE_MAKE_PROGRAM = "C:\path\to\ninja.exe"
$env:CC = "C:\path\to\mingw\bin\gcc.exe"
$env:CXX = "C:\path\to\mingw\bin\g++.exe"
pip install . --no-build-isolation
```

### Running tests

```bash
pip install ".[test]"
pytest python/tests/
```

## Quick Start

```python
import numpy as np
import hypercube_hopfield as hh

# Create a network with 256 neurons (dim=8)
net = hh.HopfieldNetwork(dim=8, seed=42)

# Store some patterns
patterns = np.random.randn(10, net.num_vertices).astype(np.float32)
net.store_patterns(patterns)

# Recall from a noisy cue
cue = patterns[0] + np.random.randn(net.num_vertices).astype(np.float32) * 0.3
recalled, steps, converged = net.recall(cue)

print(f"Converged: {converged}, steps: {steps}")
print(f"Energy before: {net.energy(cue):.4f}")
print(f"Energy after:  {net.energy(recalled):.4f}")
```

---

## API Reference

### The `dim` parameter

`dim` controls the hypercube dimension. The network has N = 2^dim neurons
(vertices on a dim-dimensional Boolean hypercube). Supported values: **4-16**.

| dim | N (neurons) | Typical use |
|-----|-------------|-------------|
| 4   | 16          | Unit tests |
| 6   | 64          | Quick experiments |
| 8   | 256         | Demos, small datasets |
| 10  | 1,024       | Medium workloads |
| 12  | 4,096       | Research scale |
| 14  | 16,384      | Large-scale |
| 16  | 65,536      | Maximum capacity |

### Enums

#### `UpdateMode`

| Value | Description |
|-------|-------------|
| `UpdateMode.Sync` | Simultaneous double-buffered updates. Deterministic and GPU-portable. **Default.** |
| `UpdateMode.Async` | Sequential random-order updates. Guaranteed monotonic energy descent. |

### HopfieldNetwork

#### Constructor

```python
hh.HopfieldNetwork(
    dim: int,
    *,
    seed: int = 0,
    reach: int = 0,
    beta: float = 4.0,
    neighbor_fraction: float = 1.0,
    tolerance: float = 1e-6,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dim` | int | *(required)* | Hypercube dimension, 4-16. N = 2^dim neurons. |
| `seed` | int | 0 | RNG seed for update order permutations. |
| `reach` | int | 0 | Hamming-ball radius (1 to dim). 0 = auto (dim // 2, ~50-63% connectivity). |
| `beta` | float | 4.0 | Inverse temperature for softmax attention. Higher = sharper recall. |
| `neighbor_fraction` | float | 1.0 | Fraction of Hamming ball to use, in (0.0, 1.0]. Sorted by distance, truncated. |
| `tolerance` | float | 1e-6 | Convergence threshold. Sweep is stable when no vertex changes more than this. |

All parameters except `dim` are keyword-only.

#### Core Methods

##### `store_pattern(pattern)`

Store a single pattern.

```python
net.store_pattern(np.array([...], dtype=np.float32))
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | ndarray | 1D array of N floats. Auto-converted to float32. |

##### `store_patterns(patterns)`

Store multiple patterns from a 2D array.

```python
patterns = np.random.randn(10, net.num_vertices).astype(np.float32)
net.store_patterns(patterns)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `patterns` | ndarray | 2D array, shape `(M, N)`. Each row is stored as a pattern. |

##### `recall(cue, *, max_steps=100, mode=UpdateMode.Sync)`

Recall a stored pattern from a (possibly noisy) cue. The input is **not modified**
-- a clean copy is returned.

```python
recalled, steps, converged = net.recall(noisy_cue)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cue` | ndarray | *(required)* | 1D array of N floats. |
| `max_steps` | int | 100 | Maximum update sweeps. |
| `mode` | UpdateMode | Sync | Update strategy. |

**Returns:** `tuple[ndarray, int, bool]`
- `recalled` -- The cleaned state, shape `(N,)`.
- `steps` -- Number of update sweeps performed.
- `converged` -- True if stabilized within `tolerance`.

##### `energy(state)`

Compute the modern Hopfield energy for a state.

```python
e = net.energy(state)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | ndarray | 1D array of N floats. |

**Returns:** `float` -- Energy value. Lower = closer to a stored pattern.

**Raises:** `ValueError` if no patterns are stored.

#### Pattern Management

##### `get_pattern(idx)`

Read back a stored pattern by index. Returns a copy.

```python
pat = net.get_pattern(0)
```

##### `pop_pattern()`

Remove the most recently stored pattern.

##### `clear()`

Remove all stored patterns and reset internal state.

##### `patterns` (property)

All stored patterns as a read-only 2D array.

```python
all_pats = net.patterns  # shape (num_patterns, num_vertices)
```

Returns `(0, N)` if no patterns are stored.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `dim` | int | Hypercube dimension. |
| `num_vertices` | int | Number of neurons (2^dim). |
| `num_patterns` | int | Number of stored patterns. |
| `seed` | int | RNG seed from construction. |
| `reach` | int | Hamming-ball radius (resolved, not 0). |
| `neighbor_fraction` | float | Fraction of Hamming ball used. |
| `beta` | float | Inverse temperature. |
| `tolerance` | float | Convergence threshold. |

All properties are read-only.

---

## Input Data Layout

All pattern and state arrays are **1D float32** with length `num_vertices` (= 2^dim).
Values are continuous (not binary). Higher-precision inputs (float64) are automatically
converted to float32 with standard NumPy casting rules.

For batch operations, `store_patterns()` accepts a **2D array** of shape
`(num_patterns, num_vertices)`, row-major (C-contiguous).

## Error Handling

| Error | When |
|-------|------|
| `ValueError("dim must be...")` | `dim` outside [4, 16] |
| `ValueError("pattern size...")` | Array length != `num_vertices` |
| `ValueError("no patterns stored")` | `energy()` with zero patterns |
| `IndexError` | `get_pattern(idx)` with `idx >= num_patterns` |
| `IndexError` | `pop_pattern()` on empty network |

All validation happens at the Python boundary before entering C++, producing
clear error messages with actual vs. expected values.

## Model Persistence

Networks can be saved and loaded via pickle or the convenience methods:

```python
# Save
net.save("model.pkl")

# Load
net = hh.HopfieldNetwork.load("model.pkl")
```

**What is saved:** Constructor configuration (dim, seed, reach, beta,
neighbor_fraction, tolerance) and all stored patterns.

**What is NOT saved:** Internal buffers (transposed pattern cache, thread pool
state). These are rebuilt on load.

Pickle protocol:

```python
import pickle
data = pickle.dumps(net)
loaded = pickle.loads(data)
```

## Limitations

- **Not thread-safe.** A single `HopfieldNetwork` instance must not be accessed
  from multiple threads concurrently. Create separate instances for parallel use.
  The GIL is released during `recall()` and `energy()` to allow other Python
  threads to run.

- **float32 precision.** All computation uses single-precision. This is by design:
  the softmax attention mechanism introduces noise that exceeds float32 rounding
  error, so double precision would add cost with no accuracy benefit.

- **Pattern memory.** At dim=16, each pattern is 256 KB. Storing 1,000 patterns
  uses ~256 MB. The `patterns` property copies all patterns into a new ndarray.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | >= 1.21 | Array I/O |
| pybind11 | >= 2.13 | Build-time only (C++ binding) |
| scikit-build-core | >= 0.10 | Build-time only (CMake integration) |
