#include "bit.hpp"
#include "mult.hpp"
#include "stdlib.h"
#include "stdio.h"
#include "assert.h"

bit x1[262], x2[262], y[131], z[131];
void randomize() {
    for (int i = 0; i < 262; i++) {
        x1[i] = bit(rand());
        x2[i] = bit(rand());
    }
    for (int i = 0; i < 131; i++) {
        y[i] = bit(rand());
        z[i] = bit(rand());
    }
}

bool check(bit* a, bit* b, size_t depth) {
    bool result = true;
    for (size_t i = 0; i < depth; i++) {
        if (!(a[i] == b[i])) {
            printf("Different at %lu\n", i);
            result = false;
        }
    }
    return result;
}

int main(int argc, char** argv) {
    puts("mult4");
    for (int i = 0; i < 1000; i++) {
        randomize();
        dmult4(x1, y, z);
        mult4(x2, y, z);
        assert(check(x1, x2, 7));
    }

    puts("karatmult8");
    for (int i = 0; i < 1000; i++) {
        randomize();
        dmult8(x1, y, z);
        karatmult8(x2, y, z);
        assert(check(x1, x2, 15));
    }

    puts("mult8");
    for (int i = 0; i < 1000; i++) {
        randomize();
        dmult8(x1, y, z);
        mult8(x2, y, z);
        assert(check(x1, x2, 15));
    }

    puts("mult16");
    puts("karatmult16");
    for (int i = 0; i < 1000; i++) {
        randomize();
        dmult16(x1, y, z);
        karatmult16(x2, y, z);
        assert(check(x1, x2, 31));
    }
    puts("mult16");
    for (int i = 0; i < 1000; i++) {
        randomize();
        dmult16(x1, y, z);
        mult16(x2, y, z);
        assert(check(x1, x2, 31));
    }
}
