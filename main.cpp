#include "Diagnostics.h"

int main()
{
    constexpr size_t DIM = 8;
    constexpr size_t N = 1ULL << DIM;

    const bool pass = RunDiagnostics<DIM>(256 * N);  // deep capacity probe
    return pass ? 0 : 1;
}
