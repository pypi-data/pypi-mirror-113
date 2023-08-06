---
title: Lexicographic Encoding
---

# Lexicographic Encoding
Easily encode tuples of primitive types to bytestrings preserving lexicographic encoding.
This means that you can later order the resulting bytestring and you will maintain the order of tuples.

## Use Cases
Typically key-value stores only allow to use bytestrings as keys, which are a little awkward to work with if one
needs a bit of structure on them.
For example LevelDB offers a custom comparator to deal with such a situation, but many other storages do not.

This package allows you to free from such constraint, using an encoding that maintains the inherent ordering.

## Stability
The project is to be considered beta.
The provided API won't change, but it has not been tested in real-world yet (it has a big automated test suite though).

Any feedback will be appreciated.
For any question or bug report please [open an issue](https://gitlab.com/dlnet/lexicographic-encoding/).

## Quick Example
```python
from lexicographic_encoding import lexpackb, lexunpackb, is_prefix_of

# Then pack everything preserving lexicographic order
# The following are all True
lexpackb(-1) > lexpackb(-2)
lexpackb(102) > lexpackb(20)
lexpackb(("Tom", 109)) > lexpackb(("Tom", 18))
```

## Documentation
Documentation of the project can be found [here](https://dlnet.gitlab.io/lexicographic-encoding/).
