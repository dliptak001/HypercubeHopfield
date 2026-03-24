# HypercubeHopfield

A Hopfield network built on a Boolean hypercube graph.

Licensed under the [Apache License 2.0](LICENSE).

## What is a Hopfield Network?

A Hopfield network is a recurrent neural network that functions as content-addressable
(associative) memory. It stores patterns as attractors of its energy landscape, and
retrieves them by converging from noisy or partial cues to the nearest stored pattern.

The network consists of N binary neurons with symmetric connection weights. Given a
set of patterns to memorize, the weights are set via Hebbian learning so that each
pattern becomes a local energy minimum. Recall is performed by initializing the network
with a corrupted cue and iterating the update rule until convergence.

## What is HypercubeHopfield?

HypercubeHopfield is a Hopfield network implementation where the connectivity is
defined by a Boolean hypercube graph of dimension DIM, giving N = 2^DIM vertices
(neurons). Each vertex's neighbors are computed by XOR operations on vertex indices --
no adjacency list is stored, and neighbor lookup is a single instruction.

The sparse hypercube topology replaces the traditional fully-connected Hopfield
architecture with a structured sparse graph, trading storage capacity for
computational efficiency and scalable memory.

The system is designed for DIM 5-10 (32 to 1024 neurons).

## Building and Running

**Requirements:** C++23 compiler (GCC 13+, Clang 16+, MSVC 19.36+), CMake 3.20+.

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/HypercubeHopfield
```

OpenMP is used for parallelism where beneficial. The build system detects MinGW,
GCC/Clang, and MSVC automatically.

## Project Structure

```
HypercubeHopfield/
  HopfieldNetwork.h/cpp  Hypercube Hopfield network (N = 2^DIM vertices)
  main.cpp               Entry point / benchmark suite

  readout/               (reserved for readout/classification layers)

  examples/              (example applications)

  diagnostics/           (benchmark and analysis tools)

  docs/
    HopfieldNetwork.md   Network architecture and parameters
```

## Documentation

| Document | Covers |
|----------|--------|
| [docs/HopfieldNetwork.md](docs/HopfieldNetwork.md) | Hypercube graph, connectivity, update rule, learning rules, parameters |
