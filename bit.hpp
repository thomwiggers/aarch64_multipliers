#ifndef BIT_H
#define BIT_H


#include <arm_neon.h>
#include <stdint.h>

#define bit_SLICES 128

typedef uint32x4_t vec;

class bit {
  vec x;
public:
  inline bit() { }
  inline bit(vec u) { x = u; }
  inline bit(int u) { x = vdupq_n_u32(-u); }
  inline bit& operator=(const bit &a) { x = a.x; return *this; }
  inline int rep(int pos) const { return 1 & (((unsigned char *) &x)[pos / 8] >> (pos & 7)); }
  inline void set(int pos) { ((unsigned char *) &x)[pos / 8] |= (1 << (pos & 7)); }
  inline void clear(int pos) { ((unsigned char *) &x)[pos / 8] &= ~(1 << (pos & 7)); }
  inline friend bit operator+(const bit &a,const bit &b) {
#ifdef countoperations
    ++cpucycles_xor;
#endif
    return a.x ^ b.x;
  }
  inline friend bit operator^(const bit &a,const bit &b) {
#ifdef countoperations
    ++cpucycles_xor;
#endif
    return a.x ^ b.x;
  }
  inline void operator+=(const bit &b) {
#ifdef countoperations
    ++cpucycles_xor;
#endif
    x ^= b.x;
  }
  inline void operator^=(const bit &b) {
#ifdef countoperations
    ++cpucycles_xor;
#endif
    x ^= b.x;
  }
  inline friend bit operator*(const bit &a,const bit &b) {
#ifdef countoperations
    ++cpucycles_and;
#endif
    return a.x & b.x;
  }
  inline friend bit operator&(const bit &a,const bit &b) {
#ifdef countoperations
    ++cpucycles_and;
#endif
    return a.x & b.x;
  }
  inline void operator&=(const bit &b) {
#ifdef countoperations
    ++cpucycles_and;
#endif
    x &= b.x;
  }
  inline void operator*=(const bit &b) {
#ifdef countoperations
    ++cpucycles_and;
#endif
    x &= b.x;
  }
  inline void setzero() { x = vdupq_n_u32(0); }
  int isnotall1(void) {
    vec ones = vdupq_n_u32((uint32_t) 0xffffffff);
    vec result_vec = vceqq_u32(x, ones);
    uint16x4_t result_16 = vqmovn_u32(result_vec);
    uint64_t bits = (uint64_t) vreinterpret_u64_u16(result_16);
    return !(bits == 0);
  }
  bool operator==(const bit &b) {
      vec result_vec = vceqq_u32(x, b.x);
      uint16x4_t result_16 = vqmovn_u32(result_vec);
      uint64_t bits = (uint64_t) vreinterpret_u64_u16(result_16);
      return !(bits == 0);
  }
};

#endif
