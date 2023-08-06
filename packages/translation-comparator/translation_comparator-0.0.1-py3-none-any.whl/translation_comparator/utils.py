# -*- coding: utf-8 -*-

from typing import Iterable


def is_unique(x: Iterable, finite: bool = False):
    if finite:  # XXX: needs to check so it will not allocate too much data
        seen = tuple(x)
    else:
        seen = list()

    return not any(i in seen or seen.append(i) for i in x)
