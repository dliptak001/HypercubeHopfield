# Hopfield Network Architecture

## Overview

The `HopfieldNetwork<DIM>` implements a Hopfield associative memory on a DIM-dimensional
Boolean hypercube with N = 2^DIM vertices (neurons).

## Hypercube Connectivity

Each vertex v has 2*DIM neighbors, computed inline via XOR masks:

- **DIM Hamming-shell connections:** cumulative-bit selectors (1, 3, 7, 15, ...)
- **DIM nearest-neighbor connections:** single-bit flips (1<<0, 1<<1, ...)

No adjacency list is stored. Neighbor lookup is O(1) via bitwise XOR.

## Update Rule

Each vertex stores a binary spin s_v in {+1, -1}. The local field at vertex v is:

    h_v = sum_j w_vj * s_j

where the sum runs over the 2*DIM neighbors of v. The vertex updates as:

    s_v <- sign(h_v)

Updates are asynchronous (one vertex at a time, random order) to guarantee
monotonic energy descent.

## Energy Function

    E = -0.5 * sum_{v,j} w_vj * s_v * s_j

The asynchronous update rule guarantees E is non-increasing at every step.
Convergence occurs when no vertex changes sign.

## Learning Rule

Patterns are stored via outer-product (Hebbian) learning:

    w_vj += (1/N) * p_v * p_j

for each pattern p. This is additive — each new pattern modifies the existing weights.

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| DIM       | Hypercube dimension (5-10) | Template parameter |
| rng_seed  | Random seed for update order | Required |
| max_steps | Maximum recall sweeps | 100 |

## Capacity

Classical Hopfield capacity on a fully-connected graph is ~0.14N patterns.
The sparse hypercube topology will have lower capacity — characterizing this
tradeoff is a key goal of this project.
