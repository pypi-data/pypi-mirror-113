#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from distutils.extension import Extension
from pathlib import Path
from typing import Iterable

from Cython.Build import cythonize

from ..comparison_helpers import compare_cythonized
from ..pair_finders import pairs_and_extentions_for_cython
from . import settings


def cythonize_paths(paths: Iterable[Path], **kwargs) -> None:

    if "module_list" in kwargs:
        raise ValueError("module_list should not be present")

    kwargs.update(build_dir=str(settings.build_dir), annotate=True)

    cythonize(list(map(str, paths)), **kwargs)


def cythonize_and_compare(*patterns: str, **kwargs):
    pairs, py_paths, pyx_paths = pairs_and_extentions_for_cython(*patterns)
    build_dir = settings.build_dir

    settings.build_dir = build_dir.joinpath(settings.py_dir)  # dirty singleton
    cythonize_paths(py_paths, **kwargs)

    settings.build_dir = build_dir.joinpath(settings.pyx_dir)
    cythonize_paths(pyx_paths, **kwargs)

    settings.build_dir = build_dir
    compare_cythonized(pairs)
