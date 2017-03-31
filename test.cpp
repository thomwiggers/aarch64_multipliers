#include "bit.hpp"
#include "mult.hpp"
#include "stdlib.h"
#include "stdio.h"

# define assert(check) \
    if (!check) { puts("ERROR"); return 1;}

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

bool check(bit* a, bit* b, long depth) {
    bool result = true;
    long first_wrong = -1;
    for (long i = 0; i < depth; i++) {
        if (!(a[i] == b[i])) {
            if (first_wrong == -1) 
                first_wrong = i;
            result = false;
        } else {
            if (first_wrong >= 0) {
                printf("Different at %ld — %ld\n", first_wrong, i-1);
                first_wrong = -1;
            }
        }
    }
    if (first_wrong != -1) {
        printf("Different at %l — %l\n", first_wrong, depth-1);
    }
    return result;
}

const int tests = 100;

int main(int argc, char** argv) {
    puts("mult4");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult4(x1, y, z);
        mult4(x2, y, z);
        assert(check(x1, x2, 7));
    }

    puts("karatmult8");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult8(x1, y, z);
        karatmult8(x2, y, z);
        assert(check(x1, x2, 15));
    }

    puts("mult8");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult8(x1, y, z);
        mult8(x2, y, z);
        assert(check(x1, x2, 15));
    }

    puts("karatmult16");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult16(x1, y, z);
        karatmult16(x2, y, z);
        assert(check(x1, x2, 31));
    }
    puts("mult16");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult16(x1, y, z);
        mult16(x2, y, z);
        assert(check(x1, x2, 31));
    }

    puts("karatmult32");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult32(x1, y, z);
        karatmult32(x2, y, z);
        assert(check(x1, x2, 63));
    }

    puts("cmult32.cpp");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult32(x1, y, z);
        cmult32(x2, y, z);
        assert(check(x1, x2, 63));
    }

    puts("mult32");
    for (int i = 0; i < tests; i++) {
        randomize();
        dmult32(x1, y, z);
        mult32(x2, y, z);
        assert(check(x1, x2, 63));
    }
}
