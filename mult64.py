from aarchimate import (start_file, Register, start_function, end_function,
                        do_xor as reg_do_xor, unload as reg_unload)

from mult32 import mult32 as multK

N = 64
OUT = 2 * N - 1
K = N//2
KOUT = 2 * K - 1


def mult64(f, g, h,
           sp,
           keep=None):

    keep = keep or []

    stack_offset = 0
    STACK_SIZE = 4032
    sp.subi(sp, STACK_SIZE)

    # Sanity checks:
    for reg in h:
        if reg.pointer is None and reg not in keep:
            raise ValueError(f"Can't throw away result {h}!")

    def do_op(op, name, i1, i2, drop=None):
        if drop is not None:
            if i1 in drop and i1 in keep:
                drop.remove(i1)
            if i2 in drop and i2 in keep:
                drop.remove(i2)
        return op(name, i1, i2, drop)

    def do_xor(*args, **kwargs):
        return do_op(reg_do_xor, *args, **kwargs)

    def unload(*registers):
        reg_unload(*[register for register in registers
                     if register not in keep])

    l = [Register(f'l{N}_{i}') for i in range(KOUT)]

    for i in range(K):
        l[i].pointer = h[i].pointer
        l[i].offset = h[i].offset
    for i in range(K, KOUT):
        l[i].pointer = sp
        l[i].offset = stack_offset
        stack_offset += 16

    sp_c = Register('spc', type='x')
    sp_c.mov(sp)
    multK(f[:K], g[:K], l[:KOUT], sp_c)

    print(f"// first done mult{N}")

    hbar = [Register(f'Hbar{N}_{i}') for i in range(KOUT)]
    for i in range(K-1):
        hbar[i].pointer, hbar[i].offset = sp, stack_offset
        stack_offset += 16
    for i in range(K-1, KOUT):
        hbar[i].pointer, hbar[i].offset = h[N + i].pointer, h[N+i].offset

    print(f"// mult{K} upper part")
    multK(f[K:], g[K:], hbar, sp_c)
    for i in range(K-1, KOUT):
        if hbar[i] in Register.stored():
            h[N+i].mark_stored()

    hbar[0].load()
    for i in range(0, N - K - 1):
        l[K+i].load()
        if i > 0:
            hbar[i-1].store()
            unload(hbar[i-1])
        hbar[i].xor(hbar[i], l[K+i], [l[K+i]])
        if i < N - K - 2:
            hbar[i+1].load()

    hbar[N-K-2].store()
    unload(hbar[N-K-2])

    Fm = [Register(f'Fm{N}_{i}') for i in range(K)]
    Gm = [Register(f'Gm{N}_{i}') for i in range(K)]
    for r in Fm + Gm:
        r.pointer, r.offset = sp, stack_offset
        stack_offset += 16

    f[0].load()
    f[K].load()

    for i in range(0, K):
        if i < K-1:
            f[i+1].load()
            f[i+K+1].load()
        else:
            g[0].load()
            g[K].load()
        Fm[i].xor(f[i], f[K+i], [f[i], f[i+K]])
        if i > 0:
            Fm[i-1].store()
            Fm[i-1].unload()

    for i in range(K):
        if i < K-1:
            g[i+1].load()
            g[i+K+1].load()
        Gm[i].xor(g[i], g[K+i], [g[i], g[i+K]])
        if i < 1:
            Fm[K-1+i].store()
            Fm[K-1+i].unload()
        else:
            Gm[i-1].store()
            Gm[i-1].unload()

    Gm[K-1].store()
    Gm[K-1].unload()

    m = [Register(f'M{N}_{i}') for i in range(KOUT)]
    for r in m:
        r.pointer, r.offset = sp, stack_offset
        stack_offset += 16

    multK(Fm, Gm, m, sp_c)

    U = [Register(f'U{N}_{i}') for i in range(KOUT)]
    for u in U:
        u.pointer = sp
        u.offset = stack_offset
        stack_offset += 16
    l[0].load()
    m[0].load()
    for i in range(K):
        if i < K-1:
            l[i+1].load()
            m[i+1].load()
        else:
            hbar[0].load()
        if i > K-20:
            U[i-1].store()
            unload(U[i-1])
        U[i].xor(l[i], m[i], [l[i], m[i]])
    for i in range(K):
        U[i].load()
        hbar[i+1].load()
        h[i+K].xor(U[i], hbar[i], [hbar[i], U[i]])
        if i >= 1:
            h[i+K-1].store()
            unload(h[i+K-1])
    h[KOUT].store()
    unload(h[KOUT])
    for i in range(K-1):
        hbar[i].load()
        if i < K-2:
            hbar[i+K+1].load()
        else:
            m[K].load()
        if i > K-20:
            U[K+i-1].store()
            unload(U[K+i-1])
        U[K+i].xor(hbar[i], hbar[i+K], [hbar[i], hbar[i+K]])

    for i in range(K-1):
        U[K+i].load()
        if i < K-2:
            m[K+i+1].load()
        if i >= 1:
            h[i+N-1].store()
            unload(h[i+N-1])
        h[i+N].xor(U[K+i], m[K+i], [U[K+i], m[K+i]])

    h[OUT - K - 1].store()
    unload(h[OUT - K - 1])

    Register.debug()

    sp.addi(sp, STACK_SIZE)
    stack_offset -= STACK_SIZE
    assert stack_offset  == 0, f"Stack offset still {stack_offset} > 0"


if __name__ == '__main__':
    start_file()

    h_pointer = Register('h', type='x', register='x0')
    h = [Register(f'h{i}', pointer=h_pointer, offset=i*16) for i in range(OUT)]

    f_pointer = Register('f', type='x', register='x1')
    f = [Register(f'f{i}', pointer=f_pointer, offset=i*16) for i in range(N)]

    g_pointer = Register('g', type='x', register='x2')
    g = [Register(f'g{i}', pointer=g_pointer, offset=i*16) for i in range(N)]

    start_function(f'mult{N}', [h_pointer, f_pointer, g_pointer],
                   f + g)
    sp = Register.get('sp')
    vector_stack_space_needed = 8
    sp.subi(sp, vector_stack_space_needed * 16)
    q = [Register.get(f'q{i}') for i in range(8, 16)]
    for i in range(0, vector_stack_space_needed):
        q[i].pointer = sp
        q[i].offset = i * 16
        q[i].store()
        q[i].unload()

    Register.debug()
    mult64(f, g, h, sp)

    for i in range(vector_stack_space_needed):
        q[i].load()
    sp.addi(sp, vector_stack_space_needed * 16)
    Register.debug()
    end_function()
