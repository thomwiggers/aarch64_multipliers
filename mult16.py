from aarchimate import (start_file, Register, start_function, end_function,
                        do_xor as reg_do_xor, unload as reg_unload)

from mult8 import mult8


def mult16(f, g, h,
           sp,
           keep=None,
           add_in=None):
    print("// " + "+" * 80)
    print("// " + "+" + " " * 16 + "mult16")
    print("// " + "+" * 80)

    keep = keep or []
    add_in = add_in or dict()

    stack_offset = 0
    STACK_SIZE = 10 * 16
    if add_in != dict():
        STACK_SIZE += 8 * 16
    sp.subi(sp, STACK_SIZE)

    # Sanity checks:
    for reg in h:
        if reg.pointer is None and reg not in keep:
            raise ValueError(f"Can't throw away result {reg}!")

    def do_op(op, name, i1, i2, drop=None):
        if drop is not None:
            if i1 in drop and i1 in keep:
                drop.remove(i1)
            if i2 in drop and i2 in keep:
                drop.remove(i2)
        return op(name, i1, i2, drop)

    def do_xor(*args, **kwargs):
        return do_op(reg_do_xor, *args, **kwargs)

    def try_load_add_for(name):
        if add_in.get(name):
            add_in[name].load()

    def do_add_in(target, register, name, *drop):
        if add_in.get(name):
            target.xor(register, add_in[name], [*drop, add_in[name]])

    def maybe_store_added_in(name, register):
        if add_in.get(name):
            register.store()
            register.unload()

    def unload(*registers):
        reg_unload(*[register for register in registers
                     if register not in keep])

    l = [Register(f'l16_{i}') for i in range(15)]

    keep_these = []
    T = 8
    if add_in.get('h0'):
        for i in range(8):
            keep_these.append(l[i])
            l[i].pointer = sp
            l[i].offset = stack_offset
            stack_offset += 16
    else:
        for i in range(0, 8):
            if h[i].pointer is None:
                keep_these.append(l[i])
            else:
                l[i].pointer = h[i].pointer
                l[i].offset = h[i].offset

    keep_these.extend(l[8:12])
    T = 12
    for i in range(T, 15):
        l[i].pointer = sp
        l[i].offset = stack_offset
        stack_offset += 16
    mult8(*(f[:8]), *(g[:8]), *l, keep=keep_these)
    try_load_add_for('h0')
    for i in range(8):
        if (l[i] in Register.stored() and
                l[i].pointer == h[i].pointer and l[i].offset == h[i].offset):
            h[i].mark_stored()
        if f'h{i}' in add_in:
            if i < 7:
                try_load_add_for(f'h{i+1}')
            print(f"// adding in into: {h[i]} = {l[i]} + %s" % add_in[f'h{i}'])
            do_add_in(h[i], l[i], f'h{i}', l[i])
            if i > 0:
                maybe_store_added_in(f'h{i-1}', h[i-1])
    maybe_store_added_in('h7', h[7])

    hbar = [Register(f'Hbar16_{i}') for i in range(15)]
    for i in range(0, 7):
        hbar[i].pointer, hbar[i].offset = sp, stack_offset
        stack_offset += 16
    for i in range(7, 15):
        hbar[i].pointer, hbar[i].offset = h[16+i].pointer, h[16+i].offset

    print("// mult8 upper part")
    mult8(*f[8:], *g[8:], *hbar,
          keep=[f[8], f[9],  f[12], f[15], g[13]],
          add_in={f'h{i}': l[8+i] for i in range(7)})
    print("//bla!")
    Register.debug()
    for i in range(7, 15):
        if hbar[i] in Register.stored():
            h[16+i].mark_stored()

    Fm = [Register(f'Fm16_{i}') for i in range(8)]

    Gm = [Register(f'Gm16_{i}') for i in range(8)]

    f[0].load()
    f[1].load()
    Fm[0].xor(f[0], f[8], [f[0], f[8]])

    for i in range(1, 8):
        if i < 7:
            f[i+1].load()
            f[i+8+1].load()
        if i == 7:
            g[0].load()
            g[8].load()
        Fm[i].xor(f[i], f[8+i], [f[i], f[i+8]])

    for i in range(8):
        if i < 7:
            g[i+1].load()
            g[i+8+1].load()
        Gm[i].xor(g[i], g[8+i], [g[i], g[i+8]])

    m = [Register(f'M16_{i}') for i in range(15)]
    l[0].load()
    mult8(*Fm, *Gm, *m,
          keep=m)

    U = [Register(f'U16_{i}') for i in range(15)]
    for i in range(8):
        if i < 7:
            l[i+1].load()
        if i == 7:
            hbar[0].load()
            try_load_add_for('h8')
        U[i].xor(l[i], m[i], [l[i], m[i]])

    for i in range(8):
        hbar[i+1].load()
        if i > 0:
            print("// Trying to add to thing")
            do_add_in(h[i+8-1], h[i+8-1], f'h{i+8-1}')
        try_load_add_for(f'h{i+8+1}')
        h[i+8].xor(U[i], hbar[i], [U[i]])
        if i >= 1:
            h[i+8-1].store()
            unload(h[i+8-1])
    h[15].store()
    # unload hbar[7] as it's not dropped by the below code
    unload(h[15], hbar[7])
    for i in range(7):
        if i < 6:
            try_load_add_for(f'h{i+16}')
            hbar[i+8+1].load()
        U[8+i].xor(hbar[i], hbar[i+8], [hbar[i], hbar[i+8]])
    for i in range(7):
        if i >= 1:
            h[i+16-1].store()
            unload(h[i+16-1])
        h[i+16].xor(U[8+i], m[8+i], [U[8+i], m[8+i]])

    h[22].store()
    unload(h[22])



    sp.addi(sp, STACK_SIZE)
    stack_offset -= STACK_SIZE
    assert stack_offset  == 0, f"Stack offset still {stack_offset} > 0"

    print("// " + "*" * 80)
    print("// " + "*" + " " * 16 + "mult16")
    print("// " + "*" * 80)

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

    mult16(f, g, h, sp)

    for i in range(vector_stack_space_needed):
        q[i].load()
    sp.addi(sp, vector_stack_space_needed * 16)
    Register.debug()
    end_function()
