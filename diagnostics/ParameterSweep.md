# ParameterSweep Results

## What is ParameterSweep?

Characterizes how the two key parameters affect network capacity:
- **reach** (1-8): number of Hamming-shell connections per vertex, added
  on top of DIM=8 nearest-neighbor connections. More shells = richer
  long-range context for the softmax attention mechanism.
- **beta** (inverse temperature): controls softmax sharpness. Higher beta
  gives more winner-take-all retrieval; lower beta gives softer blending.

For each (reach, beta) pair, a mini capacity probe finds the largest
pattern count with mean overlap >= 0.90 at 20% noise.

---

Run: DIM=8 | N=256 | noise=20% | 3-seed avg {42,1042,2042}
Reach values: {1, 2, 3, 5, 8} | Beta values: {1, 2, 4, 8, 16}

## Results

| reach | b=1    | b=2    | b=4    | b=8    | b=16   |
|-------|--------|--------|--------|--------|--------|
|   1   |  2/  4 |  2/  3 |  4/  4 |  4/ 12 |  2/  4 |
|   2   |  4/  4 |  4/  4 |  4/  5 |  4/  4 |  4/  4 |
|   3   |  4/  4 |  4/  4 |  4/  4 |  4/  4 |  4/  4 |
|   5   |  8/  5 |  8/  5 |  8/ 13 |  8/ 10 |  8/  5 |
|   8   | 16/  5 | 16/  8 | 16/  5 | 16/  5 | 16/ 10 |

(format: capacity / avg_sweeps | capacity = max patterns with overlap >= 90%)
Result: **(informational)**

## Findings

- **Reach effect:** More Hamming shells provide richer local context for the
  softmax attention, generally increasing capacity — but with diminishing
  returns as the signal-to-noise ratio saturates.
- **Beta effect:** Higher beta sharpens retrieval (closer to winner-take-all),
  which typically improves capacity up to a point. Very high beta can cause
  instability if the local similarity signal is noisy.
- **Interaction:** The optimal beta depends on reach — sparser connectivity
  (low reach) benefits from lower beta to smooth out the noisy local signal,
  while richer connectivity (high reach) can exploit higher beta.
