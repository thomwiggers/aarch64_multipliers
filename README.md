# AArch64 Binary Polynomial multipliers

This repository contains some highly optimised refined reduced Karatsuba multipliers for binary polynomials.
These are generated from Python scripts, optimised for Cortex-A53.

## Included

* Python scripts to generate assembly files
* A test program to validate that they work correctly
* A benchmarking program to compare speeds
* Karatsuba implementations in C
* C Implementations of multiplication from [Dan Bernstein's site](djbmult)

## Dependencies

* Python 3.6
* The python package [Aarchimate]

[Aarchimate]: https://github.com/thomwiggers/aarchimate
[djbmult]: https://binary.cr.yp.to/m.html
