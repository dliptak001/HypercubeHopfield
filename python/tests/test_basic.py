"""Smoke tests for the hypercube_hopfield Python SDK."""

import pickle
import numpy as np
import pytest

import hypercube_hopfield as hh
from hypercube_hopfield import HopfieldNetwork, UpdateMode


# ── Helpers ──

def random_pattern(n, rng):
    return rng.standard_normal(n).astype(np.float32)


def overlap(a, b):
    """Cosine similarity."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ── Tests ──

class TestConstruction:
    @pytest.mark.parametrize("dim", range(4, 17))
    def test_all_dims(self, dim):
        net = HopfieldNetwork(dim=dim, seed=1)
        assert net.dim == dim
        assert net.num_vertices == 2**dim
        assert net.num_patterns == 0

    def test_invalid_dim_low(self):
        with pytest.raises(ValueError, match="dim must be"):
            HopfieldNetwork(dim=3)

    def test_invalid_dim_high(self):
        with pytest.raises(ValueError, match="dim must be"):
            HopfieldNetwork(dim=17)

    def test_defaults(self):
        net = HopfieldNetwork(dim=6)
        assert net.reach == 3  # dim // 2
        assert net.beta == pytest.approx(4.0)
        assert net.neighbor_fraction == pytest.approx(1.0)
        assert net.tolerance == pytest.approx(1e-6)
        assert net.seed == 0

    def test_custom_config(self):
        net = HopfieldNetwork(
            dim=8, seed=99, reach=2, beta=2.5,
            neighbor_fraction=0.5, tolerance=1e-4,
        )
        assert net.dim == 8
        assert net.seed == 99
        assert net.reach == 2
        assert net.beta == pytest.approx(2.5)
        assert net.neighbor_fraction == pytest.approx(0.5)
        assert net.tolerance == pytest.approx(1e-4)

    def test_repr(self):
        net = HopfieldNetwork(dim=6, seed=1)
        r = repr(net)
        assert "dim=6" in r
        assert "N=64" in r


class TestStoreAndRecall:
    def test_store_single(self):
        net = HopfieldNetwork(dim=6, seed=1)
        pat = random_pattern(64, np.random.default_rng(42))
        net.store_pattern(pat)
        assert net.num_patterns == 1

    def test_store_multiple(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        for _ in range(5):
            net.store_pattern(random_pattern(64, rng))
        assert net.num_patterns == 5

    def test_recall_perfect(self):
        net = HopfieldNetwork(dim=6, seed=1)
        pat = random_pattern(64, np.random.default_rng(42))
        net.store_pattern(pat)
        recalled, steps, converged = net.recall(pat)
        assert converged
        assert overlap(recalled, pat) > 0.99

    def test_recall_noisy(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        pat = random_pattern(64, rng)
        net.store_pattern(pat)
        noise = rng.standard_normal(64).astype(np.float32) * 0.3
        recalled, steps, converged = net.recall(pat + noise)
        assert overlap(recalled, pat) > 0.95

    def test_recall_returns_tuple(self):
        net = HopfieldNetwork(dim=6, seed=1)
        pat = random_pattern(64, np.random.default_rng(42))
        net.store_pattern(pat)
        result = net.recall(pat)
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert isinstance(result[0], np.ndarray)
        assert isinstance(result[1], int)
        assert isinstance(result[2], bool)

    def test_recall_does_not_mutate_input(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        pat = random_pattern(64, rng)
        net.store_pattern(pat)
        cue = pat + rng.standard_normal(64).astype(np.float32) * 0.5
        cue_copy = cue.copy()
        net.recall(cue)
        np.testing.assert_array_equal(cue, cue_copy)

    def test_recall_async(self):
        net = HopfieldNetwork(dim=6, seed=1)
        pat = random_pattern(64, np.random.default_rng(42))
        net.store_pattern(pat)
        recalled, steps, converged = net.recall(pat, mode=UpdateMode.Async)
        assert overlap(recalled, pat) > 0.99

    def test_recall_no_patterns(self):
        net = HopfieldNetwork(dim=6, seed=1)
        cue = random_pattern(64, np.random.default_rng(42))
        recalled, steps, converged = net.recall(cue)
        assert steps == 0


class TestEnergy:
    def test_energy_decreases_on_recall(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        pat = random_pattern(64, rng)
        net.store_pattern(pat)
        noisy = pat + rng.standard_normal(64).astype(np.float32) * 0.5
        e_before = net.energy(noisy)
        recalled, _, _ = net.recall(noisy)
        e_after = net.energy(recalled)
        assert e_after <= e_before + 1e-5  # small tolerance for float

    def test_energy_no_patterns(self):
        net = HopfieldNetwork(dim=6, seed=1)
        state = random_pattern(64, np.random.default_rng(42))
        with pytest.raises(ValueError, match="no patterns"):
            net.energy(state)


class TestPatternManagement:
    def test_get_pattern_roundtrip(self):
        net = HopfieldNetwork(dim=6, seed=1)
        pat = random_pattern(64, np.random.default_rng(42))
        net.store_pattern(pat)
        retrieved = net.get_pattern(0)
        np.testing.assert_allclose(retrieved, pat, atol=1e-7)

    def test_patterns_property(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        pats = [random_pattern(64, rng) for _ in range(3)]
        for p in pats:
            net.store_pattern(p)
        all_pats = net.patterns
        assert all_pats.shape == (3, 64)
        for i, p in enumerate(pats):
            np.testing.assert_allclose(all_pats[i], p, atol=1e-7)

    def test_patterns_empty(self):
        net = HopfieldNetwork(dim=6, seed=1)
        assert net.patterns.shape == (0, 64)

    def test_pop_pattern(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        net.store_pattern(random_pattern(64, rng))
        net.store_pattern(random_pattern(64, rng))
        assert net.num_patterns == 2
        net.pop_pattern()
        assert net.num_patterns == 1

    def test_clear(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        for _ in range(5):
            net.store_pattern(random_pattern(64, rng))
        net.clear()
        assert net.num_patterns == 0

    def test_store_patterns_batch(self):
        net = HopfieldNetwork(dim=6, seed=1)
        rng = np.random.default_rng(42)
        batch = rng.standard_normal((4, 64)).astype(np.float32)
        net.store_patterns(batch)
        assert net.num_patterns == 4
        np.testing.assert_allclose(net.get_pattern(2), batch[2], atol=1e-7)


class TestErrorHandling:
    def test_store_wrong_size(self):
        net = HopfieldNetwork(dim=6, seed=1)
        with pytest.raises((ValueError, RuntimeError)):
            net.store_pattern(np.zeros(100, dtype=np.float32))

    def test_recall_wrong_size(self):
        net = HopfieldNetwork(dim=6, seed=1)
        net.store_pattern(np.zeros(64, dtype=np.float32))
        with pytest.raises((ValueError, RuntimeError)):
            net.recall(np.zeros(100, dtype=np.float32))

    def test_energy_wrong_size(self):
        net = HopfieldNetwork(dim=6, seed=1)
        net.store_pattern(np.zeros(64, dtype=np.float32))
        with pytest.raises((ValueError, RuntimeError)):
            net.energy(np.zeros(100, dtype=np.float32))

    def test_get_pattern_out_of_range(self):
        net = HopfieldNetwork(dim=6, seed=1)
        with pytest.raises((IndexError, RuntimeError)):
            net.get_pattern(0)

    def test_pop_empty(self):
        net = HopfieldNetwork(dim=6, seed=1)
        with pytest.raises((IndexError, RuntimeError)):
            net.pop_pattern()

    def test_store_patterns_wrong_shape(self):
        net = HopfieldNetwork(dim=6, seed=1)
        with pytest.raises(ValueError):
            net.store_patterns(np.zeros(64, dtype=np.float32))  # 1D, not 2D

    def test_store_patterns_wrong_width(self):
        net = HopfieldNetwork(dim=6, seed=1)
        with pytest.raises(ValueError, match="num_vertices"):
            net.store_patterns(np.zeros((3, 100), dtype=np.float32))


class TestPersistence:
    def test_pickle_roundtrip(self):
        net = HopfieldNetwork(dim=6, seed=42)
        rng = np.random.default_rng(42)
        for _ in range(3):
            net.store_pattern(random_pattern(64, rng))
        data = pickle.dumps(net)
        loaded = pickle.loads(data)
        assert loaded.dim == 6
        assert loaded.num_patterns == 3
        np.testing.assert_allclose(
            loaded.patterns, net.patterns, atol=1e-7,
        )

    def test_pickle_preserves_config(self):
        net = HopfieldNetwork(
            dim=8, seed=99, reach=2, beta=2.5,
            neighbor_fraction=0.5, tolerance=1e-4,
        )
        loaded = pickle.loads(pickle.dumps(net))
        assert loaded.seed == 99
        assert loaded.reach == 2
        assert loaded.beta == pytest.approx(2.5)
        assert loaded.neighbor_fraction == pytest.approx(0.5)
        assert loaded.tolerance == pytest.approx(1e-4)

    def test_save_load(self, tmp_path):
        net = HopfieldNetwork(dim=6, seed=42)
        pat = random_pattern(64, np.random.default_rng(42))
        net.store_pattern(pat)
        path = tmp_path / "model.pkl"
        net.save(path)
        loaded = HopfieldNetwork.load(path)
        assert loaded.num_patterns == 1
        np.testing.assert_allclose(loaded.get_pattern(0), pat, atol=1e-7)

    def test_pickle_empty(self):
        net = HopfieldNetwork(dim=6, seed=1)
        loaded = pickle.loads(pickle.dumps(net))
        assert loaded.num_patterns == 0
        assert loaded.dim == 6

    def test_load_wrong_type(self, tmp_path):
        path = tmp_path / "bad.pkl"
        with open(path, "wb") as f:
            pickle.dump("not a network", f)
        with pytest.raises(TypeError, match="HopfieldNetwork"):
            HopfieldNetwork.load(path)


class TestConvenience:
    def test_dtype_coercion(self):
        """float64 arrays are automatically converted to float32."""
        net = HopfieldNetwork(dim=6, seed=1)
        pat = np.random.default_rng(42).standard_normal(64)  # float64
        net.store_pattern(pat)
        assert net.num_patterns == 1

    def test_version(self):
        assert hasattr(hh, "__version__")
        assert hh.__version__ == "0.1.0"
