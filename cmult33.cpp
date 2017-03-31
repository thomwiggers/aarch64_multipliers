#include "bit.hpp"
#include "stdlib.h"
#include "mult.hpp"
#include "stdio.h"

void cmult33(bit* r, const bit* f, const bit* g) {
    // compute upper part
    // sets r[0 .. 32] correctly, produces stuff we need to add into
    mult32(r, f, g);

    bit f32 = f[32];
    const unsigned int n = 32;
    for (int i = 0; i < n-1; i++) {
        r[32+i] += f32 * g[i];
    }
    r[63] = f32 * g[31];

    bit g32 = g[32];
    for (int i = 0; i < n; i++) {
        r[32+i] += g32 * f[i];
    }

    r[64] = f32 * g32;
}
