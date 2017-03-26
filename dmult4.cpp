#include "bit.hpp"

void dmult4(bit* h, const bit* f, const bit* g) {
    bit t1 = f[3] * g[3];
    bit t2 = f[3] * g[0];
    bit t3 = f[3] * g[1];
    bit t4 = f[3] * g[2];
    bit t5 = f[0] * g[3];
    bit t6 = f[1] * g[3];
    bit t7 = f[2] * g[3];
    bit t8 = f[2] * g[2];
    bit t9 = f[2] * g[0];
    bit t10 = f[2] * g[1];
    bit t11 = f[0] * g[2];
    bit t12 = f[1] * g[2];
    bit t13 = f[1] * g[1];
    bit t14 = f[1] * g[0];
    bit t15 = f[0] * g[1];
    bit t16 = f[0] * g[0];
    bit t17 = t15 + t14;
    bit t18 = t13 + t11;
    bit t19 = t18 + t9;
    bit t20 = t12 + t10;
    bit t21 = t20 + t5;
    bit t22 = t8 + t6;
    bit t23 = t21 + t2;
    bit t24 = t22 + t3;
    bit t25 = t7 + t4;
    h[0] = t16;
    h[1] = t17;
    h[2] = t19;
    h[3] = t23;
    h[4] = t24;
    h[5] = t25;
    h[6] = t1;
}

