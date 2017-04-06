#include "bit.hpp"
#include "stdlib.h"
#include "mult.hpp"
#include "stdio.h"

void cmult64(bit* r, const bit* f, const bit* g) {
    const int n = 64, k = n/2;
    // step 1
    // Load lower part
    // noop in C, of course
    // step 2
    // L = F_l * G_l
    mult32(r, f, g);
   
    // step 5
    bit absa[k];
    bit absb[k];
    
    // abs doesn't exist in binary polynomials, so just add
    for (int i = 0; i < k; i++)
        absa[i] = f[i] + f[i+k];
    for (int i = 0; i < k; i++)
        absb[i] = g[i] + g[i+k];

    // step 6
    bit hbar[n-1];
    mult32(hbar, f+k, g+k);
    // add in upper part of L to lower part of H
    for (int i = 0; k+i < n-1; i++) {
        hbar[i] += r[k+i];
    }

    // step 7
    bit m[n-1];
    mult32(m, absa, absb);

    // step 8
    bit u[n-1];
    // U_0 .. U_{k-1} = l_0, ..., l_{k-1}
    for (int i = 0; i < k; i++)
        u[i] = r[i];
    // U_k .. U_{n-1} = (h_0, ..., h_{k-2})
    for (int i = 0; i < k-1; i++)
        u[k+i] = hbar[i]; 
    // U += Hbar
    for (int i = 0; i < n-1; i++)
        u[i] += hbar[i];

    // step 9
    for (int i = 0; i < n-1; i++)
        u[i] += m[i];

    // step 10
    for (int i = 0; i < n-1; i++)
        r[k+i] = u[i];

    // step 11: no carry

    // step 12
    for (int i = k-1; i < n-1; i++)
        r[n + i] = hbar[i];
    
}
