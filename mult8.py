from aarchimate import (start_file, Register, start_function, end_function,
                        do_xor as reg_do_xor, unload as reg_unload)

from mult4 import mult4


def mult8(f0, f1, f2, f3, f4, f5, f6, f7,
          g0, g1, g2, g3, g4, g5, g6, g7,
          h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14,
          keep=None,
          add_in=None):

    print("//===============================================================")
    print("//                        Mult8                                  ")
    print("//===============================================================")

    keep = keep or []
    add_in = add_in or dict()

    # Sanity checks:
    for h in (h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14):
        if h.pointer is None and h not in keep:
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

    def do_add_in(target, register, name):
        if add_in.get(name):
            target.xor(register, add_in[name], [add_in[name]])

    def try_load_add_for(name):
        if add_in.get(name):
            add_in[name].load()

    def unload(*registers):
        reg_unload(*[register for register in registers
                     if register not in keep])


    def maybe_store(register):
        if register.pointer:
            register.store()
            unload(register)

    if add_in.get('h0'):
        l0 = Register('l0')
    else:
        l0 = Register('l0', pointer=h0.pointer, offset=h0.offset)
    if add_in.get('h1'):
        l1 = Register('l1')
    else:
        l1 = Register('l1', pointer=h1.pointer, offset=h1.offset)
    if add_in.get('h2'):
        l2 = Register('l2')
    else:
        l2 = Register('l2', pointer=h2.pointer, offset=h2.offset)
    if add_in.get('h3'):
        l3 = Register('l3')
    else:
        l3 = Register('l3', pointer=h3.pointer, offset=h3.offset)
    l4 = Register('l4')
    l5 = Register('l5')
    l6 = Register('l6')
    mult4(f0, f1, f2, f3,
          g0, g1, g2, g3,
          l0, l1, l2, l3, l4, l5, l6,
          keep=[f0, f1, f2, f3, f4,
                g0, g1, g2, g3, g4,
                l0, l1, l2, l3, l4, l5, l6, *keep])
    for h, l in [(h0, l0), (h1, l1), (h2, l2), (h3, l3)]:
        if l in Register.stored():
            h.mark_stored()

    if add_in.get('h0'):
        add_in['h0'].load()
    if add_in.get('h1'):
        add_in['h1'].load()
    if add_in.get('h0'):
        h0.xor(l0, add_in['h0'], [add_in['h0']])
    if add_in.get('h2'):
        add_in['h2'].load()
    if add_in.get('h1'):
        h1.xor(l1, add_in['h1'], [add_in['h1']])
    if add_in.get('h3'):
        add_in['h3'].load()
    if add_in.get('h0'):
        maybe_store(h0)
    if add_in.get('h2'):
        h2.xor(l2, add_in['h2'], [add_in['h2']])
    if add_in.get('h1'):
        maybe_store(h1)
    if add_in.get('h3'):
        h3.xor(l3, add_in['h3'], [add_in['h3']])
    if add_in.get('h2'):
        maybe_store(h2)

    f4.load()
    f5.load()
    # Fm = F_l + F_h
    Fm0 = do_xor('Fm0', f0, f4, [f0])
    del f0
    f6.load()
    Fm1 = do_xor('Fm1', f1, f5, [f1])
    del f1
    f7.load()
    Fm2 = do_xor('Fm2', f2, f6, [f2])
    del f2
    g4.load()
    Fm3 = do_xor('Fm3', f3, f7, [f3])
    del f3
    g5.load()
    Gm0 = do_xor('Gm0', g0, g4, [g0])
    del g0
    g6.load()
    Gm1 = do_xor('Gm1', g1, g5, [g1])
    del g1
    g7.load()
    Gm2 = do_xor('Gm2', g2, g6, [g2])
    if add_in.get('h3'):
        # Store h3 by delay
        maybe_store(h3)
    del g2
    Gm3 = do_xor('Gm3', g3, g7, [g3])
    del g3

    # Hbar = A_h * B_h + (l_k, l_n-2)
    Hbar = [Register(f'hbar{i}') for i in range(7)]
    Hbar[3].pointer, Hbar[3].offset = h11.pointer, h11.offset
    Hbar[4].pointer, Hbar[4].offset = h12.pointer, h12.offset
    Hbar[5].pointer, Hbar[5].offset = h13.pointer, h13.offset
    Hbar[6].pointer, Hbar[6].offset = h14.pointer, h14.offset
    mult4(f4, f5, f6, f7,
          g4, g5, g6, g7,
          *Hbar,
          keep=[*Hbar],
          add_in={'h0': l4, 'h1': l5, 'h2': l6})
    del l4, l5, l6
    # Compute M = (F_l + F_h) * (G_l * G_h)

    M = [Register(f'M{i}') for i in range(7)]
    mult4(Fm0, Fm1, Fm2, Fm3,
          Gm0, Gm1, Gm2, Gm3,
          *M, keep=[*M])

    U0 = Register('U0')
    U1 = Register('U1')
    U2 = Register('U2')
    U3 = Register('U3')
    U4 = Register('U4')
    U5 = Register('U5')
    U6 = Register('U6')

    def bla(U, l, x, h):
        if h in keep:
            U.xor(l, x)
            h.rename(l)
        else:
            U.xor(l, x, [l])
    bla(U0, l0, Hbar[0], h0)
    try_load_add_for('h4')
    bla(U1, l1, Hbar[1], h1)
    try_load_add_for('h5')
    h4.xor(U0, M[0], [M[0], U0])
    h5.xor(U1, M[1], [M[1], U1])
    del U0, U1
    do_add_in(h4, h4, 'h4')
    try_load_add_for('h6')
    bla(U2, l2, Hbar[2], h2)
    maybe_store(h4)
    do_add_in(h5, h5, 'h5')
    bla(U3, l3, Hbar[3], h3)
    maybe_store(h5)
    h6.xor(U2, M[2], [M[2], U2])
    try_load_add_for('h7')
    h7.xor(U3, M[3], [M[3], U3])
    do_add_in(h6, h6, 'h6')
    do_add_in(h7, h7, 'h7')
    maybe_store(h6)
    U4.xor(Hbar[0], Hbar[4], [Hbar[0]])
    maybe_store(h7)
    U5.xor(Hbar[1], Hbar[5], [Hbar[1]])
    U6.xor(Hbar[2], Hbar[6], [Hbar[2]])
    U4.xor(U4, M[4], [M[4]])
    h9.xor(U5, M[5], [M[5], U5])
    h8.rename(U4)
    maybe_store(h8)
    h10.xor(U6, M[6], [M[6], U6])
    maybe_store(h9)
    maybe_store(h10)

    h11.rename(Hbar[3])
    h12.rename(Hbar[4])
    h13.rename(Hbar[5])
    h14.rename(Hbar[6])

    unload(h11, h12, h13, h14)

    print("//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("//                  END   Mult8                                  ")
    print("//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

if __name__ == '__main__':
    start_file()

    h_pointer = Register('h', type='x', register='x0')
    h0 = Register('h0', pointer=h_pointer, offset=0)
    h1 = Register('h1', pointer=h_pointer, offset=1*16)
    h2 = Register('h2', pointer=h_pointer, offset=2*16)
    h3 = Register('h3', pointer=h_pointer, offset=3*16)
    h4 = Register('h4', pointer=h_pointer, offset=4*16)
    h5 = Register('h5', pointer=h_pointer, offset=5*16)
    h6 = Register('h6', pointer=h_pointer, offset=6*16)
    h7 = Register('h7', pointer=h_pointer, offset=7*16)
    h8 = Register('h8', pointer=h_pointer, offset=8*16)
    h9 = Register('h9', pointer=h_pointer, offset=9*16)
    h10 = Register('h10', pointer=h_pointer, offset=10*16)
    h11 = Register('h11', pointer=h_pointer, offset=11*16)
    h12 = Register('h12', pointer=h_pointer, offset=12*16)
    h13 = Register('h13', pointer=h_pointer, offset=13*16)
    h14 = Register('h14', pointer=h_pointer, offset=14*16)

    f_pointer = Register('f', type='x', register='x1')
    f0 = Register('f0', pointer=f_pointer, offset=0)
    f1 = Register('f1', pointer=f_pointer, offset=1*16)
    f2 = Register('f2', pointer=f_pointer, offset=2*16)
    f3 = Register('f3', pointer=f_pointer, offset=3*16)
    f4 = Register('f4', pointer=f_pointer, offset=4*16)
    f5 = Register('f5', pointer=f_pointer, offset=5*16)
    f6 = Register('f6', pointer=f_pointer, offset=6*16)
    f7 = Register('f7', pointer=f_pointer, offset=7*16)

    g_pointer = Register('g', type='x', register='x2')
    g0 = Register('g0', pointer=g_pointer, offset=0)
    g1 = Register('g1', pointer=g_pointer, offset=1*16)
    g2 = Register('g2', pointer=g_pointer, offset=2*16)
    g3 = Register('g3', pointer=g_pointer, offset=3*16)
    g4 = Register('g4', pointer=g_pointer, offset=4*16)
    g5 = Register('g5', pointer=g_pointer, offset=5*16)
    g6 = Register('g6', pointer=g_pointer, offset=6*16)
    g7 = Register('g7', pointer=g_pointer, offset=7*16)

    start_function('mult8', [h_pointer, f_pointer, g_pointer],
                   [f0, f1, f2, f3, f4, f5, f6, f7,
                    g0, g1, g2, g3, g4, g5, g6, g7])
    sp = Register.get('sp')
    vector_stack_space_needed = 8
    sp.subi(sp, vector_stack_space_needed * 16)
    q = [Register.get(f'q{i}') for i in range(8, 16)]
    for i in range(0, vector_stack_space_needed):
        q[i].pointer = sp
        q[i].offset = i * 16
        q[i].store()
        q[i].unload()

    mult8(f0, f1, f2, f3, f4, f5, f6, f7,
          g0, g1, g2, g3, g4, g5, g6, g7,
          h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14)
    Register.debug()

    for i in range(vector_stack_space_needed):
        q[i].load()
    sp.addi(sp, vector_stack_space_needed * 16)
    Register.debug()
    end_function()
