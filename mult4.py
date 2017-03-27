from library import (
    start_file, Register, start_function, end_function, do_and as reg_do_and,
    do_xor as reg_do_xor,
    unload as reg_unload)

# based on https://binary.cr.yp.to/m.html


def mult4(f0, f1, f2, f3,
          g0, g1, g2, g3,
          h0, h1, h2, h3, h4, h5, h6,
          add_in=None,
          keep=None):
    keep = keep or []
    add_in = add_in or dict()

    # Sanity checks:
    for h in (h0, h1, h2, h3, h4, h5, h6):
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

    def do_and(*args, **kwargs):
        return do_op(reg_do_and, *args, **kwargs)

    def do_add_in(register, name):
        if name in add_in:
            register.xor(register, add_in[name])
            add_in[name].unload()

    def unload(*registers):
        reg_unload(*[register for register in registers
                     if register not in keep])

    f3.load()
    g3.load()
    g0.load()
    t1 = do_and('t1', f3, g3)
    g1.load()
    t2 = do_and('t2', f3, g0)
    g2.load()
    f0.load()
    t4 = do_and('t4', f3, g2)
    f1.load()
    t5 = do_and('t5', f0, g3)
    f2.load()
    t6 = do_and('t6', f1, g3)
    h6.rename(t1)
    if h6.pointer:
        h6.store()
        unload(h6)
    del t1
    t7 = do_and('t7', f2, g3, [g3])
    t8 = do_and('t8', f2, g2)
    t25 = do_xor('t25', t7, t4, [t4, t7])
    del t4, t7
    t9 = do_and('t9', f2, g0)
    h5.rename(t25)
    if h5.pointer:
        h5.store()
        unload(h5)
    del t25
    t22 = do_xor('t22', t8, t6, [t6, t8])
    del t6, t8
    t10 = do_and('t10', f2, g1, [f2])
    del f2
    t11 = do_and('t11', f0, g2)
    t12 = do_and('t12', f1, g2, [g2])
    del g2
    t13 = do_and('t13', f1, g1)
    t14 = do_and('t14', f1, g0, [f1])
    t20 = do_xor('t20', t12, t10, [t10, t12])
    del t10, t12, f1
    t16 = do_and('t16', f0, g0, [g0])
    del g0
    t15 = do_and('t15', f0, g1, [f0])
    del f0
    do_add_in(t16, 'h0')
    t18 = do_xor('t18', t13, t11, [t11, t13])
    del t11, t13
    h0.rename(t16)
    if h0.pointer:
        h0.store()
        unload(h0)
    del t16
    t19 = do_xor('t19', t18, t9, [t9, t18])
    del t9, t18
    t21 = do_xor('t21', t20, t5, [t20, t5])
    do_add_in(t19, 'h2')
    del t5, t20
    t17 = do_xor('t17', t15, t14, [t14, t15])
    del t14, t15
    t23 = do_xor('t23', t21, t2, [t2, t21])
    do_add_in(t23, 'h3')
    del t2, t21
    h2.rename(t19)
    if h2.pointer:
        h2.store()
        unload(h2)
    del t19
    t3 = do_and('t3', f3, g1, [f3, g1])
    del f3, g1
    h3.rename(t23)
    if h3.pointer:
        h3.store()
        unload(h3)
    del t23
    do_add_in(t17, 'h1')
    t24 = do_xor('t24', t22, t3, [t22, t3])
    del t22, t3
    h1.rename(t17)
    if h1.pointer:
        h1.store()
        unload(h1)
    del t17
    h4.rename(t24)
    if h4.pointer:
        h4.store()
        unload(h4)
    del t24


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

    f_pointer = Register('f', type='x', register='x1')
    f0 = Register('f0', pointer=f_pointer, offset=0)
    f1 = Register('f1', pointer=f_pointer, offset=1*16)
    f2 = Register('f2', pointer=f_pointer, offset=2*16)
    f3 = Register('f3', pointer=f_pointer, offset=3*16)

    g_pointer = Register('g', type='x', register='x2')
    g0 = Register('g0', pointer=g_pointer, offset=0)
    g1 = Register('g1', pointer=g_pointer, offset=1*16)
    g2 = Register('g2', pointer=g_pointer, offset=2*16)
    g3 = Register('g3', pointer=g_pointer, offset=3*16)

    start_function('mult4', [h_pointer, f_pointer, g_pointer],
                   [f0, f1, f2, f3, g0, g1, g2, g3])
    mult4(f0, f1, f2, f3, g0, g1, g2, g3,
          h0, h1, h2, h3, h4, h5, h6)
    Register.debug()
    end_function()
