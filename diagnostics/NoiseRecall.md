# NoiseRecall Results

## What is NoiseRecall?

Measures the network's ability to recover a stored pattern from a noisy cue.
A single pattern is stored, then corrupted at varying noise levels (percentage
of bits flipped). The network runs Recall() and the overlap (normalized dot
product) between the recalled state and the original is measured. An overlap
of 1.0 means perfect recall; 0.0 means uncorrelated.

Pass criteria: overlap >= 0.95 at 10% noise, >= 0.90 at 20%, >= 0.80 at 30%.
40% and 50% are reported but not judged (marked --).

---

Run: reach=DIM/2 | beta=4.0 | 3-seed avg {42,1042,2042}

## Summary

| DIM | N    | Connections | 10%    | 20%    | 30%    | 40%    | 50%    | Sweeps | Result |
|-----|------|-------------|--------|--------|--------|--------|--------|--------|--------|
| 4   | 16   | 10          | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.7-2.0 | PASS  |
| 5   | 32   | 15          | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 2.0    | PASS   |
| 6   | 64   | 41          | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 2.0    | PASS   |
| 7   | 128  | 63          | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 2.0    | PASS   |
| 8   | 256  | 162         | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 2.0    | PASS   |

## DIM=4 (N=16, reach=2, 10 connections)

| Noise | Overlap | Sweeps | Result |
|-------|---------|--------|--------|
|   10% |  1.0000 |    1.7 |  PASS  |
|   20% |  1.0000 |    2.0 |  PASS  |
|   30% |  1.0000 |    2.0 |  PASS  |
|   40% |  1.0000 |    2.0 |   --   |
|   50% |  1.0000 |    2.0 |   --   |

## DIM=5 (N=32, reach=2, 15 connections)

| Noise | Overlap | Sweeps | Result |
|-------|---------|--------|--------|
|   10% |  1.0000 |    2.0 |  PASS  |
|   20% |  1.0000 |    2.0 |  PASS  |
|   30% |  1.0000 |    2.0 |  PASS  |
|   40% |  1.0000 |    2.0 |   --   |
|   50% |  1.0000 |    2.0 |   --   |

## DIM=6 (N=64, reach=3, 41 connections)

| Noise | Overlap | Sweeps | Result |
|-------|---------|--------|--------|
|   10% |  1.0000 |    2.0 |  PASS  |
|   20% |  1.0000 |    2.0 |  PASS  |
|   30% |  1.0000 |    2.0 |  PASS  |
|   40% |  1.0000 |    2.0 |   --   |
|   50% |  1.0000 |    2.0 |   --   |

## DIM=7 (N=128, reach=3, 63 connections)

| Noise | Overlap | Sweeps | Result |
|-------|---------|--------|--------|
|   10% |  1.0000 |    2.0 |  PASS  |
|   20% |  1.0000 |    2.0 |  PASS  |
|   30% |  1.0000 |    2.0 |  PASS  |
|   40% |  1.0000 |    2.0 |   --   |
|   50% |  1.0000 |    2.0 |   --   |

## DIM=8 (N=256, reach=4, 162 connections)

| Noise | Overlap | Sweeps | Result |
|-------|---------|--------|--------|
|   10% |  1.0000 |    2.0 |  PASS  |
|   20% |  1.0000 |    2.0 |  PASS  |
|   30% |  1.0000 |    2.0 |  PASS  |
|   40% |  1.0000 |    2.0 |   --   |
|   50% |  1.0000 |    2.0 |   --   |

## Findings

- **Perfect recall at all noise levels, all DIMs.** Every configuration achieves
  1.0000 overlap even at 50% corruption (half the bits flipped). The modern Hopfield
  softmax attention with Hamming-ball connectivity creates extremely deep attractor
  basins for single-pattern recall.
- **Single-pattern recall is trivially easy.** With only 1 stored pattern, the
  softmax attention has no competing patterns to confuse it — every neighbor's
  similarity points to the same pattern. This test validates basic correctness
  rather than probing capacity limits (see CapacityProbe for that).
- **Convergence is uniformly fast.** 2 sweeps across all DIMs and noise levels
  (1.7 at DIM=4/10% where fewer bits need correcting). The network snaps to the
  stored pattern almost immediately.
- **Even DIM=4 (16 vertices, 10 connections) handles 50% noise perfectly** for
  single-pattern recall. The capacity limitation at small DIM only appears when
  storing multiple patterns.
