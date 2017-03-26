#include "bit.hpp"

void dmult8(bit* h, const bit* f, const bit* g) {
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
bit t26 = f[7] * g[7];
bit t27 = f[7] * g[4];
bit t28 = f[7] * g[5];
bit t29 = f[7] * g[6];
bit t30 = f[4] * g[7];
bit t31 = f[5] * g[7];
bit t32 = f[6] * g[7];
bit t33 = f[6] * g[6];
bit t34 = f[6] * g[4];
bit t35 = f[6] * g[5];
bit t36 = f[4] * g[6];
bit t37 = f[5] * g[6];
bit t38 = f[5] * g[5];
bit t39 = f[5] * g[4];
bit t40 = f[4] * g[5];
bit t41 = f[4] * g[4];
bit t42 = t40 + t39;
bit t43 = t38 + t36;
bit t44 = t43 + t34;
bit t45 = t37 + t35;
bit t46 = t45 + t30;
bit t47 = t33 + t31;
bit t48 = t46 + t27;
bit t49 = t47 + t28;
bit t50 = t32 + t29;
bit t51 = g[0] + g[4];
bit t52 = g[1] + g[5];
bit t53 = g[2] + g[6];
bit t54 = g[3] + g[7];
bit t55 = f[0] + f[4];
bit t56 = f[1] + f[5];
bit t57 = f[2] + f[6];
bit t58 = f[3] + f[7];
bit t59 = t58 * t54;
bit t60 = t58 * t51;
bit t61 = t58 * t52;
bit t62 = t58 * t53;
bit t63 = t55 * t54;
bit t64 = t56 * t54;
bit t65 = t57 * t54;
bit t66 = t57 * t53;
bit t67 = t57 * t51;
bit t68 = t57 * t52;
bit t69 = t55 * t53;
bit t70 = t56 * t53;
bit t71 = t56 * t52;
bit t72 = t56 * t51;
bit t73 = t55 * t52;
bit t74 = t55 * t51;
bit t75 = t73 + t72;
bit t76 = t71 + t69;
bit t77 = t76 + t67;
bit t78 = t70 + t68;
bit t79 = t78 + t63;
bit t80 = t66 + t64;
bit t81 = t79 + t60;
bit t82 = t80 + t61;
bit t83 = t65 + t62;
bit t84 = t24 + t41;
bit t85 = t25 + t42;
bit t86 = t1 + t44;
bit t87 = t74 + t84;
bit t88 = t75 + t85;
bit t89 = t77 + t86;
bit t90 = t81 + t48;
bit t91 = t82 + t49;
bit t92 = t83 + t50;
bit t93 = t59 + t26;
bit t94 = t87 + t16;
bit t95 = t88 + t17;
bit t96 = t89 + t19;
bit t97 = t90 + t23;
bit t98 = t91 + t84;
bit t99 = t92 + t85;
bit t100 = t93 + t86;
h[0] = t16;
h[1] = t17;
h[2] = t19;
h[3] = t23;
h[4] = t94;
h[5] = t95;
h[6] = t96;
h[7] = t97;
h[8] = t98;
h[9] = t99;
h[10] = t100;
h[11] = t48;
h[12] = t49;
h[13] = t50;
h[14] = t26;
}

