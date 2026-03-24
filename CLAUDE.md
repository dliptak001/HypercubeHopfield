# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build

CMake project targeting C++23 with MinGW (primary), also supports GCC/Clang and MSVC. Developed in CLion.

```bash
# Configure and build (from project root)
cmake -B cmake-build-debug -DCMAKE_BUILD_TYPE=Debug
cmake --build cmake-build-debug

# Release build
cmake -B cmake-build-release -DCMAKE_BUILD_TYPE=Release
cmake --build cmake-build-release

# Run
./cmake-build-release/HypercubeHopfield.exe
```

## Architecture

Hopfield associative memory network on a Boolean hypercube (2^DIM vertices, DIM 5-10).
Each vertex stores a binary spin (+1/-1) and updates via the standard Hopfield rule
using weighted connections derived from the hypercube topology. Neighbor lookup is
a single XOR instruction — no adjacency storage. See `docs/HopfieldNetwork.md`.

Key classes:
- `HopfieldNetwork<DIM>` — network core (HopfieldNetwork.h/cpp)

## Conventions

- OpenMP is enabled for parallelism; CMakeLists.txt handles compiler-specific flags
- Source files are collected via `file(GLOB)` — new .cpp files in project root and readout/ are included
- Header guards use `#pragma once`
- All values in the pipeline are float
- Tests and diagnostics should be run in Release mode (-ffast-math can cause divergent results in Debug)
