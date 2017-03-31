from aarchimate import (start_file, Register, start_function, end_function,
                        unload)


from mult32 import mult32

N = 33
OUT = 2*33-1


def mult33(f, g, h,
           sp):

    mult32(f[:32], g[:32], h[:-2], sp, keep=h[32:])

    Register.debug()
    f[0].load()
    g[32].load()
    h[32].load()
    t = [Register(f'temp{i}') for i in range(32)]
    for i in range(31):
        if 32+i+1 < 63:
            h[32+i+1].load()
        if i > 0 and 32+i-1 < 63:
            h[32+i-1].xor(h[32+i-1], t[i-1], [t[i-1]])
        f[i+1].load()
        t[i].and_(f[i], g[32], [f[i]])

        if 0 < i < 20:
            h[32+i-1].store()
            unload(h[32+i-1])
    h[62].xor(h[62], t[30])
    f[32].load()
    h[63].and_(f[31], g[32])
    Register.debug()

    g[31].load()
    h[64].and_(f[32], g[32], [g[32]])

    for i in range(31, -1, -1):
        if i > 0:
            g[i-1].load()
        if i < 31:
            h[32+i+1].xor(h[32+i+1], t[i+1], [t[i+1]])
        if i > 0:
            h[32+i-1].load()
        t[i].and_(f[32], g[i], [g[i]])
        if i == 31:
            h[64].store()
            unload(h[64])
        else:
            h[32+i+1].store()
            unload(h[32+i+1])

    h[32].xor(h[32], t[0], [t[0]])
    h[32].store()

    Register.debug()


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
    mult33(f, g, h, sp)

    for i in range(vector_stack_space_needed):
        q[i].load()
    sp.addi(sp, vector_stack_space_needed * 16)
    Register.debug()
    end_function()
