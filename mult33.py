from aarchimate import (start_file, Register, start_function, end_function,
                        unload)


from mult32 import mult32

N = 33
OUT = 2*33-1


def mult33(f, g, h,
           sp):

    mult32(f[:32], g[:32], h[:-2], sp, keep=h[32:64])

    Register.debug()
    f[0].load()
    g[32].load()
    tf = [Register(f'temp_f_{i}') for i in range(32)]
    tg = [Register(f'temp_g_{i}') for i in range(32)]

    g[32].load()
    f[32].load()
    g[0].load()
    h[64].and_(f[32], g[32])

    for i in range(32):
        tf[i].and_(g[32], f[i], [f[i]])
        if i == 0:
            h[64].store()
            unload(h[64])
        else:
            h[i+32-1].store()
            unload(h[i+32-1])
        if i + 32 < 63:
            h[i+32].load()
        tg[i].and_(f[32], g[i], [g[i]])
        if i < 31:
            f[i+1].load()
        if i + 32 < 63:
            h[i+32].xor(h[i+32], tf[i], [tf[i]])
            g[i+1].load()
            h[i+32].xor(h[i+32], tg[i], [tg[i]])
        else:
            h[i+32].xor(tf[i], tg[i], [tf[i], tg[i]])

    h[63].store()
    unload(h[63], f[32], g[32])

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
