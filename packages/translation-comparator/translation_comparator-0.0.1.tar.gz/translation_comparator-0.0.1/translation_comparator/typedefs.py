#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import (Callable, Iterable, Iterator, List, Sequence, Tuple,
                    TypeVar, Union)

SHOW_FUNC_DATA = Sequence[Path]
SHOW_FUNC = Callable[[bool, SHOW_FUNC_DATA], None]

DIFF = List[List[str]]
DIFF_FUNC = Callable[
    [Sequence[str], Sequence[str]],
    Iterable[str]]
DIFF_ITER = Iterable[Iterable[str]]

GEN_PATH_FUNC = Callable[[Path], Tuple[Path, Path]]
PATH_FUNC = Callable[[Path], Path]


#####################################################################################################################

# from collections import abc


# ITEM = TypeVar("ITEM")
# FORABLE = Union[Iterable[ITEM], Iterator[ITEM]]
# # FORABLE[ITEM] almost == Iterator[ITEM]


# class Ior(abc.Iterator):
#     def __next__(self):
#         self.go = next(self.iter)
#         if self.go:
#             return 0
#         else:
#             raise StopIteration()

#     def __init__(self, iter):
#         self.iter = iter


# class Ile(abc.Iterable):
#     def __iter__(self):
#         return Ior(self.iter)

#     def __init__(self, iter):
#         self.iter = iter


# print(isinstance(Ior(range(10)[::-1]), abc.Iterable))
# print(isinstance(Ile(range(10)[::-1]), abc.Iterable))
