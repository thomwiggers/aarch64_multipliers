#ifndef MULT_H
#define MULT_H

#include "bit.hpp"

extern "C" { 
    extern void mult4(bit *,const bit *,const bit *);
    extern void mult8(bit *,const bit *,const bit *);
    extern void mult16(bit *,const bit *,const bit *);
    extern void mult32(bit *,const bit *,const bit *);
    extern void mult33(bit *,const bit *,const bit *);
    extern void mult64(bit *,const bit *,const bit *);
}

extern void dmult4(bit *,const bit *,const bit *);
extern void dmult8(bit *,const bit *,const bit *);
extern void dmult16(bit *,const bit *,const bit *);
extern void dmult32(bit *,const bit *,const bit *);
extern void dmult33(bit *,const bit *,const bit *);
extern void dmult64(bit *,const bit *,const bit *);
extern void karatmult8(bit *,const bit *,const bit *);
extern void karatmult16(bit *,const bit *,const bit *);
extern void karatmult32(bit *,const bit *,const bit *);
extern void karatmult64(bit *,const bit *,const bit *);
extern void cmult32(bit *,const bit *,const bit *);
extern void cmult33(bit *,const bit *,const bit *);
extern void cmult64(bit *,const bit *,const bit *);
#endif
