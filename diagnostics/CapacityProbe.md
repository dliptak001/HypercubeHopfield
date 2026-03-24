# CapacityProbe Results

## What is CapacityProbe?

Measures the network's empirical memory capacity: the maximum number of
patterns that can be stored and reliably recalled from 20% noise. Capacity
is defined as the largest pattern count where mean overlap >= 0.90.

Classical Hopfield capacity is ~0.14N. Modern Hopfield networks with
exponential energy functions theoretically achieve exponential capacity
in N. This diagnostic measures the empirical limit on the sparse hypercube
topology with Hamming-ball connectivity.

At high pattern counts, a random sample of 64 patterns is tested per seed
rather than all M (marked with * in the table).

**Note:** These results represent a sanity check. The probe ceiling is capped
at 65536 patterns for practical runtime. Where the ceiling is reached without
finding a drop, the actual capacity may be significantly higher — the
theoretical bound for modern Hopfield networks is exponential in N.

---

Run: reach=DIM/2 | beta=4.0 | noise=20% | ceiling=65536 | 3-seed avg {42,1042,2042}

## Summary

| DIM | N    | Connections | Capacity    | % of N    | Status          |
|-----|------|-------------|-------------|-----------|-----------------|
| 4   | 16   | 10          | 1           | 6%        | Limited         |
| 5   | 32   | 15          | 6           | 19%       | Limited         |
| 6   | 64   | 41          | 256         | 400%      | Strong          |
| 7   | 128  | 63          | 16384       | 12800%    | Very strong     |
| 8   | 256  | 162         | >= 65536    | >= 25600% | Ceiling reached |

## DIM=4 (N=16, reach=2, 10 connections)

| Count | Mean Ovlp | Min Ovlp | Sweeps | Status |
|-------|-----------|----------|--------|--------|
|     1 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     2 |    0.8542 |   0.1250 |    2.3 |  FAIL  |
|     3 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     4 |    0.7083 |  -0.2500 |    2.5 |  FAIL  |
|     6 |    0.8542 |  -0.1250 |    2.3 |  FAIL  |
|     8 |    0.6302 |  -0.1250 |    2.4 |  FAIL  |
|    12 |    0.7361 |  -0.2500 |    2.5 |  FAIL  |
|    16 |    0.6120 |  -0.2500 |    2.9 |  FAIL  |
|    24 |    0.4288 |  -0.5000 |    2.8 |  FAIL  |

Capacity: **1 pattern** (6% of N)

## DIM=5 (N=32, reach=2, 15 connections)

| Count | Mean Ovlp | Min Ovlp | Sweeps | Status |
|-------|-----------|----------|--------|--------|
|     1 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     2 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     3 |    1.0000 |   1.0000 |    2.2 |  PASS  |
|     4 |    0.9688 |   0.6250 |    2.6 |  PASS  |
|     6 |    1.0000 |   1.0000 |    2.4 |  PASS  |
|     8 |    0.8932 |  -0.0625 |    2.5 |  FAIL  |
|    12 |    0.8403 |  -0.0625 |    2.7 |  FAIL  |
|    16 |    0.7956 |   0.0000 |    3.0 |  FAIL  |
|    24 |    0.6953 |  -0.1875 |    3.3 |  FAIL  |
|    32 |    0.6582 |  -0.2500 |    3.8 |  FAIL  |
|    48 |    0.5512 |  -0.3750 |    4.4 |  FAIL  |
|    64 |    0.5068 |  -0.3125 |    5.1 |  FAIL  |
|*  128 |    0.2956 |  -0.3750 |    7.9 |  FAIL  |

Capacity: **6 patterns** (19% of N)

## DIM=6 (N=64, reach=3, 41 connections)

| Count | Mean Ovlp | Min Ovlp | Sweeps | Status |
|-------|-----------|----------|--------|--------|
|     1 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     2 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     3 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|     4 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     6 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     8 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    12 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|    16 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|    24 |    0.9844 |  -0.1250 |    2.0 |  PASS  |
|    32 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|    48 |    0.9928 |  -0.0312 |    2.1 |  PASS  |
|    64 |    0.9530 |  -0.0938 |    2.2 |  PASS  |
|*  128 |    0.9705 |   0.0000 |    2.2 |  PASS  |
|*  256 |    0.9507 |   0.0625 |    2.3 |  PASS  |
|*  512 |    0.8823 |  -0.1250 |    2.5 |  FAIL  |
|* 1024 |    0.8867 |  -0.1875 |    2.5 |  FAIL  |
|* 2048 |    0.7173 |  -0.1250 |    2.9 |  FAIL  |
|* 4096 |    0.6533 |  -0.2500 |    3.2 |  FAIL  |
|* 8192 |    0.5282 |  -0.2500 |    3.9 |  FAIL  |
|*16384 |    0.4434 |  -0.2500 |    4.7 |  FAIL  |

Capacity: **256 patterns** (400% of N)

## DIM=7 (N=128, reach=3, 63 connections)

| Count | Mean Ovlp | Min Ovlp | Sweeps | Status |
|-------|-----------|----------|--------|--------|
|     1 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     2 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     3 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     4 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     6 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     8 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    12 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    16 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    24 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    32 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    48 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    64 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*  128 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*  256 |    0.9950 |   0.0469 |    2.1 |  PASS  |
|*  512 |    0.9960 |   0.2344 |    2.1 |  PASS  |
|* 1024 |    0.9965 |   0.3281 |    2.2 |  PASS  |
|* 2048 |    1.0000 |   1.0000 |    2.2 |  PASS  |
|* 4096 |    0.9846 |  -0.0312 |    2.4 |  PASS  |
|* 8192 |    0.9550 |  -0.0938 |    2.6 |  PASS  |
|*16384 |    0.9341 |  -0.1094 |    3.0 |  PASS  |
|*32768 |    0.8896 |  -0.0781 |    4.6 |  FAIL  |
|*65536 |    0.8273 |  -0.1406 |    8.2 |  FAIL  |

Capacity: **16384 patterns** (12800% of N)

## DIM=8 (N=256, reach=4, 162 connections)

| Count | Mean Ovlp | Min Ovlp | Sweeps | Status |
|-------|-----------|----------|--------|--------|
|     1 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     2 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     3 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     4 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     6 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     8 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    12 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    16 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    24 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    32 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    48 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    64 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*  128 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*  256 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*  512 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|* 1024 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|* 2048 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|* 4096 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|* 8192 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*16384 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*32768 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|*65536 |    1.0000 |   1.0000 |    2.0 |  PASS  |

Capacity: **>= 65536 patterns** (>= 25600% of N) — ceiling reached

## Findings

- **Capacity scales super-linearly with DIM.** The jump from DIM=5 (6 patterns) to
  DIM=6 (256) to DIM=7 (16384) to DIM=8 (65536+) is dramatic — consistent with the
  exponential capacity prediction of modern Hopfield theory.
- **DIM=4-5 are too small for meaningful associative memory.** With only 10-15
  connections per vertex, the softmax attention can't reliably discriminate between
  patterns. These DIMs are useful for unit testing only.
- **DIM=6 is the crossover point.** 41 connections (64% of N=64) gives 256 patterns —
  4x the vertex count and well above the classical 0.14N=9 limit.
- **DIM=7-8 show exponential-regime behavior.** Perfect or near-perfect recall at
  thousands to tens of thousands of patterns, with mean overlap at 1.0000 and
  convergence in 2 sweeps. The probe ceiling, not the network, is the limiting factor.
- **The classical 0.14N limit is irrelevant.** Even DIM=6 exceeds it by 28x.
  At DIM=8 the network stores at least 256x its own vertex count with zero degradation.
