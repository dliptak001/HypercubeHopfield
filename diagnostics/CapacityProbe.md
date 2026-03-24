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

Run: reach=DIM/2 | beta=4.0 | noise=20% | ceiling=65536 | 3-seed avg {42,1042,2042} | continuous states

## Summary

| DIM | N    | Connections | Capacity    | % of N    | Status          |
|-----|------|-------------|-------------|-----------|-----------------|
| 4   | 16   | 10          | 1           | 6%        | Limited         |
| 5   | 32   | 15          | 6           | 19%       | Limited         |
| 6   | 64   | 41          | 512         | 800%      | Strong          |
| 7   | 128  | 63          | 32768       | 25600%    | Very strong     |
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
|     4 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|     6 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|     8 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    12 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|    16 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|    24 |    0.9891 |   0.2188 |    2.1 |  PASS  |
|    32 |    0.9893 |  -0.0312 |    2.2 |  PASS  |
|    48 |    0.9878 |   0.0938 |    2.2 |  PASS  |
|    64 |    0.9536 |  -0.0938 |    2.3 |  PASS  |
|*  128 |    0.9749 |   0.0312 |    2.5 |  PASS  |
|*  256 |    0.9564 |   0.0625 |    2.5 |  PASS  |
|*  512 |    0.9175 |  -0.0625 |    2.7 |  PASS  |
|* 1024 |    0.8840 |  -0.1875 |    2.8 |  FAIL  |
|* 2048 |    0.7256 |  -0.2188 |    3.3 |  FAIL  |
|* 4096 |    0.6992 |  -0.1875 |    3.5 |  FAIL  |
|* 8192 |    0.5708 |  -0.2500 |    4.3 |  FAIL  |
|*16384 |    0.4430 |  -0.3125 |    5.3 |  FAIL  |

Capacity: **512 patterns** (800% of N)

## DIM=7 (N=128, reach=3, 63 connections)

| Count | Mean Ovlp | Min Ovlp | Sweeps | Status |
|-------|-----------|----------|--------|--------|
|     1 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     2 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     3 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     4 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     6 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|     8 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    12 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|    16 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    24 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    32 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    48 |    1.0000 |   1.0000 |    2.0 |  PASS  |
|    64 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|*  128 |    1.0000 |   1.0000 |    2.1 |  PASS  |
|*  256 |    0.9950 |   0.0469 |    2.2 |  PASS  |
|*  512 |    1.0000 |   1.0000 |    2.2 |  PASS  |
|* 1024 |    1.0000 |   1.0000 |    2.3 |  PASS  |
|* 2048 |    1.0000 |   1.0000 |    2.4 |  PASS  |
|* 4096 |    0.9905 |   0.0156 |    2.6 |  PASS  |
|* 8192 |    0.9689 |  -0.0625 |    2.9 |  PASS  |
|*16384 |    0.9337 |  -0.1094 |    3.4 |  PASS  |
|*32768 |    0.9021 |  -0.1250 |    4.1 |  PASS  |
|*65536 |    0.8868 |  -0.1562 |    5.7 |  FAIL  |

Capacity: **32768 patterns** (25600% of N)

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

- **Continuous states increased capacity at DIM 6-7.** DIM=6 went from 256 (binary) to
  512 (continuous) — a 2x improvement. DIM=7 went from 16384 to 32768, also 2x. The
  continuous formulation gives the softmax more freedom to separate attractors without
  being forced into discrete states.
- **Capacity scales super-linearly with DIM.** The jump from DIM=5 (6 patterns) to
  DIM=6 (512) to DIM=7 (32768) to DIM=8 (65536+) is dramatic — consistent with the
  exponential capacity prediction of modern Hopfield theory.
- **DIM=4-5 are too small for meaningful associative memory.** With only 10-15
  connections per vertex, the softmax attention can't reliably discriminate between
  patterns. These DIMs are useful for unit testing only.
- **DIM=6 is the crossover point.** 41 connections (64% of N=64) gives 512 patterns —
  8x the vertex count and well above the classical 0.14N=9 limit.
- **DIM=8 still hits the probe ceiling** at 65536 with perfect recall — the true
  capacity is higher. The exponential capacity regime is clearly in effect.
