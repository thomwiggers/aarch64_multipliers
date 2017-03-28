from library import (start_file, Register, start_function, end_function,
                     do_xor as reg_do_xor, unload as reg_unload)

from mult8 import mult8


def mult16(f, g, h,
           sp,
           keep=None,
           add_in=None):

    keep = keep or []
    add_in = add_in or dict()

    stack_offset = 0
    STACK_SIZE = 16 * 16
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

    def do_add_in(register, name):
        if add_in.get(name):
            register.xor(register, add_in[name])
            add_in[name].unload()

    def unload(*registers):
        reg_unload(*[register for register in registers
                     if register not in keep])

    l = [Register(f'l16_{i}') for i in range(15)]
    for i in range(8):
        l[i].pointer = h[i].pointer
        l[i].offset = h[i].offset
    for i in range(8, 15):
        l[i].pointer = sp
        l[i].offset = stack_offset
        stack_offset += 16
    mult8(*(f[:8]), *(g[:8]), *l, keep=[*l[8:12]])

    hbar = [Register(f'Hbar16_{i}') for i in range(15)]
    for i in range(0, 8):
        hbar[i].pointer, hbar[i].offset = sp, stack_offset
        stack_offset += 16
    for i in range(8, 15):
        hbar[i].pointer, hbar[i].offset = h[15+i].pointer, h[15+i].offset

    print("// mult8 upper part")
    mult8(*f[8:], *g[8:], *hbar,
          keep=[f[8], f[9]],
          add_in={f'h{i}': l[8+i] for i in range(7)})

    Register.debug()

    Fm = [Register(f'Fm{i}') for i in range(8)]
    Gm = [Register(f'Gm{i}') for i in range(8)]
    for i in range(8):
        Fm[i].xor(f[i], f[8+i], [f[i]])
    for i in range(8):
        Gm[i].xor(g[i], g[8+i], [g[i]])

    sp.addi(sp, STACK_SIZE)


if __name__ == '__main__':
    start_file()

    h_pointer = Register('h', type='x', register='x0')
    h = [Register(f'h{i}', pointer=h_pointer, offset=i*16) for i in range(31)]

    f_pointer = Register('f', type='x', register='x1')
    f = [Register(f'f{i}', pointer=f_pointer, offset=i*16) for i in range(16)]

    g_pointer = Register('g', type='x', register='x2')
    g = [Register(f'g{i}', pointer=g_pointer, offset=i*16) for i in range(16)]

    start_function('mult16', [h_pointer, f_pointer, g_pointer],
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
    mult16(f, g, h, sp)

    for i in range(vector_stack_space_needed):
        q[i].load()
    sp.addi(sp, vector_stack_space_needed * 16)
    Register.debug()
    end_function()
