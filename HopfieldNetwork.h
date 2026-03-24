#pragma once

#include <cstddef>
#include <memory>
#include <vector>
#include <random>

/// Hopfield network on a DIM-dimensional Boolean hypercube (N = 2^DIM vertices).
///
/// Each vertex stores a binary spin (+1/-1) and updates via the standard Hopfield
/// rule using weighted connections derived from the hypercube topology.
///
/// Neighbor masks are computed inline from the loop index — no adjacency storage.
/// Connection weights are learned from stored patterns via Hebbian or modern
/// Hopfield learning rules.
///
/// Call StorePattern() to imprint patterns, then Recall() to converge from a
/// noisy or partial cue to the nearest stored attractor.
template <size_t DIM>
class HopfieldNetwork
{
    static_assert(DIM >= 5 && DIM <= 10, "DIM must be in 5 <= DIM <= 10");

    static constexpr size_t N = 1ULL << DIM;
    static constexpr size_t MASK = N - 1;
    static constexpr size_t NUM_CONNECTIONS = 2 * DIM;

public:
    static constexpr size_t dim = DIM;
    static constexpr size_t num_vertices = N;
    static constexpr size_t num_connections = NUM_CONNECTIONS;

    /// Inline neighbor mask computation — no stored adjacency.
    /// Shells [0..DIM):  mask = (1 << (i+1)) - 1  -> 1, 3, 7, 15, ...
    /// Nearest [0..DIM): mask = 1 << i             -> 1, 2, 4, 8, ...
    static constexpr uint32_t ShellMask(size_t i) { return (1u << (i + 1)) - 1; }
    static constexpr uint32_t NearestMask(size_t i) { return 1u << i; }

    static std::unique_ptr<HopfieldNetwork> Create(uint64_t rng_seed)
    {
        return std::unique_ptr<HopfieldNetwork>(new HopfieldNetwork(rng_seed));
    }

    HopfieldNetwork(const HopfieldNetwork&) = delete;
    HopfieldNetwork& operator=(const HopfieldNetwork&) = delete;

    /// @brief Store a pattern into the network via Hebbian learning.
    /// @param pattern Array of N floats, each +1 or -1.
    void StorePattern(const float* pattern);

    /// @brief Run asynchronous updates until convergence or max_steps.
    /// @param state In/out: N-element spin array (+1/-1). Modified in place.
    /// @param max_steps Maximum update sweeps before declaring non-convergence.
    /// @return Number of sweeps taken (< max_steps means converged).
    size_t Recall(float* state, size_t max_steps = 100);

    /// @brief Compute network energy for the given state.
    [[nodiscard]] float Energy(const float* state) const;

    /// @brief Number of patterns currently stored.
    [[nodiscard]] size_t NumPatterns() const { return num_patterns_; }

    /// @brief Clear all stored patterns (zero the weight matrix).
    void Clear();

    [[nodiscard]] const float* State() const { return vtx_state_; }

private:
    explicit HopfieldNetwork(uint64_t rng_seed);

    uint64_t rng_seed_;
    size_t num_patterns_ = 0;

    alignas(64) float vtx_state_[N]{};
    std::vector<float> vtx_weight_;  // flat [N * NUM_CONNECTIONS] connection weights

    void Initialize();
    void UpdateVertex(size_t v);
};
