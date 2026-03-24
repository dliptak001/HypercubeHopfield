#include "HopfieldNetwork.h"

#include <cstdio>

int main()
{
    constexpr size_t DIM = 7;
    auto net = HopfieldNetwork<DIM>::Create(42);

    std::printf("HypercubeHopfield DIM=%zu  N=%zu  connections=%zu\n",
                net->dim, net->num_vertices, net->num_connections);
    std::printf("Patterns stored: %zu\n", net->NumPatterns());

    return 0;
}
