from library import (start_file, Register, start_function, end_function,
                     do_xor, unload)

from mult4 import mult4


def mult8(f0, f1, f2, f3, f4, f5, f6, f7,
          g0, g1, g2, g3, g4, g5, g6, g7,
          h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14):
    l0 = Register('l0', pointer=h0.pointer, offset=h0.offset)
    l1 = Register('l1', pointer=h1.pointer, offset=h1.offset)
    l2 = Register('l2', pointer=h2.pointer, offset=h2.offset)
    l3 = Register('l3', pointer=h3.pointer, offset=h3.offset)
    l4 = Register('l4')
    l5 = Register('l5')
    l6 = Register('l6')
    mult4(f0, f1, f2, f3,
          g0, g1, g2, g3,
          l0, l1, l2, l3, l4, l5, l6,
          keep=[f0, f1, f2, f3, f4,
                g0, g1, g2, g3, g4,
                l0, l1, l2, l3, l4, l5, l6])
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
    del g2
    Gm3 = do_xor('Gm3', g3, g7, [g3])
    del g3

    # Hbar = A_h * B_h + (l_k, l_n-2)
    Hbar = [Register(f'hbar{i}') for i in range(7)]
    mult4(f4, f5, f6, f7,
          g4, g5, g6, g7,
          *Hbar,
          keep=[*Hbar],
          add_in={'h0': l4, 'h1': l5, 'h2': l6})
    del l4, l5, l6
    # Compute M = (F_l + F_h) * (G_l * G_h)

    M = [Register(f'M{i}') for i in range(7)]
    M3.pointer, M3.offset = h3.pointer, h3.offset
    M4.pointer, M4.offset = h4.pointer, h4.offset
    M5.pointer, M5.offset = h5.pointer, h5.offset
    M6.pointer, M6.offset = h6.pointer, h6.offset
    mult4(Fm0, Fm1, Fm2, Fm3,
          Gm0, Gm1, Gm2, Gm3,
          *M, keep=[*M])

    U0 = Register('U0', pointer=h4.pointer, offset=h4.offset)
    U1 = Register('U1', pointer=h5.pointer, offset=h5.offset)
    U2 = Register('U2', pointer=h6.pointer, offset=h6.offset)
    U3 = Register('U3', pointer=h7.pointer, offset=h7.offset)
    U4 = Register('U4', pointer=h8.pointer, offset=h8.offset)
    U5 = Register('U5', pointer=h9.pointer, offset=h9.offset)
    U6 = Register('U6', pointer=h10.pointer, offset=h10.offset)

    U0.xor(l0, Hbar[0])
    U1.xor(l1, Hbar[1])
    U0.xor(U0, M[0])
    U1.xor(U1, M[1])
    U0.store()
    U2.xor(l2, Hbar[2])
    U3.xor(l3, Hbar[3])
    U2.xor(U2, M[2])
    U3.xor(U3, M[3])
    U2.store()
    U4.xor(l4, Hbar[4])
    U3.store()
    U5.xor(l5, Hbar[5])
    U6.xor(l6, Hbar[6])
    U4.xor(U4, M[4])
    U5.xor(U5, M[5])
    U4.store()
    U6.xor(U6, M[6])
    U5.store()
    U6.store()

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
    mult8(f0, f1, f2, f3, f4, f5, f6, f7,
          g0, g1, g2, g3, f4, f5, f6, f7,
          h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14)
    Register.debug()
    end_function()
