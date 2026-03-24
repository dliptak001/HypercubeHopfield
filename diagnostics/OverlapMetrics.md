# OverlapMetrics Results

## What is OverlapMetrics?

Measures per-pattern recall quality and cross-pattern interference.
5 patterns are stored, each corrupted at 20% noise, recalled, and measured:
- **Target overlap**: similarity to the intended pattern (should be ~1.0)
- **Max cross overlap**: highest similarity to any other stored pattern
  (should be low — high values mean spurious attractor mixtures)

This diagnoses whether attractors are clean and well-separated, or whether
the network converges to spurious states that blend multiple patterns.

Pass: all target overlaps >= 0.90, all cross overlaps < 0.50.

---

Run: reach=DIM/2 | beta=4.0 | 5 patterns | noise=20% | 3-seed avg {42,1042,2042} | continuous states

## Summary

| DIM | N    | Connections | Avg Target | Max Cross | Result |
|-----|------|-------------|------------|-----------|--------|
| 4   | 16   | 10          | 0.9000     | +0.6667   | FAIL   |
| 5   | 32   | 15          | 0.9333     | +0.3750   | FAIL   |
| 6   | 64   | 41          | 1.0000     | +0.1771   | PASS   |
| 7   | 128  | 63          | 1.0000     | +0.1302   | PASS   |
| 8   | 256  | 162         | 1.0000     | +0.0625   | PASS   |

## DIM=4 (N=16, reach=2, 10 connections)

| Pattern | Target Ovlp | Max Cross Ovlp | Sweeps | Result |
|---------|-------------|----------------|--------|--------|
|       0 |      1.0000 |        +0.2500 |    2.7 |  PASS  |
|       1 |      1.0000 |        -0.0417 |    2.0 |  PASS  |
|       2 |      1.0000 |        +0.3333 |    2.0 |  PASS  |
|       3 |      0.7916 |        +0.6667 |    3.3 |  FAIL  |
|       4 |      0.7083 |        +0.5834 |    3.3 |  FAIL  |

Result: **FAIL** (patterns 3-4 converge to spurious blends with high cross overlap)

## DIM=5 (N=32, reach=2, 15 connections)

| Pattern | Target Ovlp | Max Cross Ovlp | Sweeps | Result |
|---------|-------------|----------------|--------|--------|
|       0 |      1.0000 |        +0.1042 |    2.7 |  PASS  |
|       1 |      1.0000 |        +0.1667 |    2.3 |  PASS  |
|       2 |      0.6667 |        +0.3750 |    2.7 |  FAIL  |
|       3 |      1.0000 |        +0.1875 |    2.3 |  PASS  |
|       4 |      1.0000 |        +0.2083 |    2.7 |  PASS  |

Result: **FAIL** (pattern 2 converges to spurious state at 0.67 overlap)

## DIM=6 (N=64, reach=3, 41 connections)

| Pattern | Target Ovlp | Max Cross Ovlp | Sweeps | Result |
|---------|-------------|----------------|--------|--------|
|       0 |      1.0000 |        +0.1667 |    2.3 |  PASS  |
|       1 |      1.0000 |        +0.0833 |    2.0 |  PASS  |
|       2 |      1.0000 |        +0.1042 |    2.0 |  PASS  |
|       3 |      1.0000 |        +0.1250 |    2.0 |  PASS  |
|       4 |      1.0000 |        +0.1771 |    2.0 |  PASS  |

Result: **PASS**

## DIM=7 (N=128, reach=3, 63 connections)

| Pattern | Target Ovlp | Max Cross Ovlp | Sweeps | Result |
|---------|-------------|----------------|--------|--------|
|       0 |      1.0000 |        +0.1302 |    2.0 |  PASS  |
|       1 |      1.0000 |        +0.0885 |    2.0 |  PASS  |
|       2 |      1.0000 |        +0.1094 |    2.0 |  PASS  |
|       3 |      1.0000 |        +0.0052 |    2.0 |  PASS  |
|       4 |      1.0000 |        +0.0521 |    2.0 |  PASS  |

Result: **PASS**

## DIM=8 (N=256, reach=4, 162 connections)

| Pattern | Target Ovlp | Max Cross Ovlp | Sweeps | Result |
|---------|-------------|----------------|--------|--------|
|       0 |      1.0000 |        +0.0495 |    2.0 |  PASS  |
|       1 |      1.0000 |        +0.0365 |    2.0 |  PASS  |
|       2 |      1.0000 |        +0.0625 |    2.0 |  PASS  |
|       3 |      1.0000 |        +0.0391 |    2.0 |  PASS  |
|       4 |      1.0000 |        +0.0417 |    2.0 |  PASS  |

Result: **PASS**

## Findings

- **DIM >= 6 shows perfect attractor separation**, identical to the binary formulation.
  All 5 patterns recalled at 1.0000 target overlap with low cross-interference.
- **DIM=4 now fails where it previously passed under binary sign activation.** Without
  sign activation snapping states to +1/-1, the continuous update produces blended
  states for patterns 3-4 (0.79 and 0.71 overlap with cross > 0.50). The binary
  formulation masked this weakness by forcing discrete attractors.
- **DIM=5 still fails on pattern 2** (0.67 overlap), same as the binary formulation.
  The sparse connectivity (15 connections, 47% of N=32) is insufficient for 5 patterns.
- **Cross-interference decreases with DIM**, as before: +0.67 (DIM=4), +0.38 (DIM=5),
  +0.18 (DIM=6), +0.13 (DIM=7), +0.06 (DIM=8).
- **The continuous formulation is slightly more demanding at small DIM.** Without the
  sign activation acting as a hard quantizer, the network must rely purely on softmax
  attention to separate attractors. This reveals the true attractor quality — DIM=4
  with 10 connections is genuinely too sparse for 5 continuous-valued patterns.
