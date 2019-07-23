# AArch64 Binary Polynomial multipliers

This repository contains some highly optimised refined reduced Karatsuba multipliers for binary polynomials.
These are generated from Python scripts, optimised for Cortex-A53.

## Referencing

See https://thomwiggers.nl/publication/armcluster/

Thom Wiggers. Energy-efficient ARM64 Cluster with Cryptanalytic Applications: 80 cores that do not cost you an ARM and a leg. LATINCRYPT 2017 (to appear).

```bibtex
@InProceedings{LATINCRYPT:Wiggers17,
    author="Wiggers, Thom",
    editor="Lange, Tanja and Dunkelman, Orr",
    title="Energy-Efficient ARM64 Cluster with Cryptanalytic Applications",
    booktitle="Progress in Cryptology -- LATINCRYPT 2017",
    year="2019",
    month=july,
    day=20,
    publisher="Springer International Publishing",
    address="Cham",
    pages="175--188",
    isbn="978-3-030-25283-0",
    doi="10.1007/978-3-030-25283-0_10",
    url="https://thomwiggers.nl/publication/armcluster/",
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
