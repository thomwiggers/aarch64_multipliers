# AArch64 Binary Polynomial multipliers

This repository contains some highly optimised refined reduced Karatsuba multipliers for binary polynomials.
These are generated from Python scripts, optimised for Cortex-A53.

## Referencing

See https://thomwiggers.nl/publication/armcluster/

Thom Wiggers. Energy-efficient ARM64 Cluster with Cryptanalytic Applications: 80 cores that do not cost you an ARM and a leg. LATINCRYPT 2017 (to appear).

```latex
@inproceedings{Wiggers2017armcluster,
  author = "Thom Wiggers",
  title = "Energy-efficient ARM64 Cluster with Cryptanalytic Applications: 80 cores that do not cost you an ARM and a leg",
  date = "2017",
  editor = "Tanja Lange and Orr Dunkelman",
  booktitle = "Progress in Cryptology - LATINCRYPT~2017: 5th International Conference on Cryptology and Information Security in Latin America",
  eventdate = {2017-10-20/2017-10/22},
  pages = {to appear},
}
```

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
