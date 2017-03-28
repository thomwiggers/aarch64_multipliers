#ifndef MULT_H
#define MULT_H

#include "bit.hpp"

extern "C" { 
    extern void mult4(bit *,const bit *,const bit *);
    extern void mult8(bit *,const bit *,const bit *);
}

extern void dmult4(bit *,const bit *,const bit *);
extern void dmult8(bit *,const bit *,const bit *);
extern void dmult16(bit *,const bit *,const bit *);
extern void karatmult8(bit *,const bit *,const bit *);
extern void karatmult16(bit *,const bit *,const bit *);
extern void karatmult16twolevel(bit *,const bit *,const bit *);

#endif
