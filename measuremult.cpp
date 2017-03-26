#include <cstdio>
#include <cstdlib>
#include "bit.hpp"
#include "mult.hpp"
#include "cpucycles.h"

#ifndef N_TESTS
#define N_TESTS 200000
#endif

long long tests[N_TESTS];

int compare(const void *a, const void *b) {
    return ((int)*(long long*) a - *(long long*)b);
}

bit x[262], y[131], z[131];
void randomize() {
    for (int i = 0; i < 262; i++)
        x[i] = bit(rand());
    for (int i = 0; i < 131; i++) {
        y[i] = bit(rand());
        z[i] = bit(rand());
    }
}

void measure(const char* name, void (*fp)(bit*, const bit*, const bit*)) {
    long long cycles, cycles2;
    printf("Measuring %s...\n", name);
    for(int i = 0; i < N_TESTS; ++i) {
        randomize();
        cycles = cpucycles();
        fp(x, y, z);
        cycles2 = cpucycles();
        tests[i] = cycles2 - cycles;
        if (i == N_TESTS/2) { 
            puts("Halfway through");
        }
    }
    
    puts("Sorting...");
    qsort(tests, N_TESTS, sizeof(long long), compare);
    // print
    printf("\tMinimum num of cycles: %lld\n", tests[0]);
    printf("\tMedian num of cycles:  %lld\n", tests[N_TESTS/2]);
    printf("\tMaximum num of cycles: %lld\n", tests[N_TESTS-1]);
    printf("\tMedian/vector size:    %lld\n", tests[N_TESTS/2]/bit_SLICES);
    puts("");

}


void testmult() {
    measure("djb mult4", dmult4);
    measure("Thom's mult4", mult4);
}


int main(const int argc, char** argv) {

    testmult();

    return 0;
}
