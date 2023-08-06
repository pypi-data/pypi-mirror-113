#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import chain
from pathlib import Path
from typing import Iterable, List, Set, Tuple

from . import cython
from .cython import settings as cython_settings
from .cython.code_comparator import (build_diff_path, build_out_path,
                                     compare_and_save_two_files_by_path)
from .path_helpers import change_same_paths_if_needed


def unique_path_list(*pairs: Iterable[Path]) -> Set[Path]:
    return set(chain(*pairs))


def compare_cythonized(pairs: Iterable[Iterable[Path]]) -> None:
    show_func = cython_settings.show_func

    if cython_settings.create_dirs:
        if not cython_settings.diff_dir.exists():
            cython_settings.diff_dir.mkdir()

        if not cython_settings.build_dir.exists():
            cython_settings.build_dir.mkdir()

    for path1, path2 in pairs:
        compare_and_save_two_files_by_path(path1, path2)

        # yes, it cannot be in the start of the loop body
        # beacuse of get_code_from_two_files_by_path
        path1, path2 = change_same_paths_if_needed(path1, path2)
        if cython_settings.save_as_diff:
            show_func(True, [build_diff_path(path1, path2)])
        else:
            show_func(False, [build_out_path(path1),
                              build_out_path(path2)])


def construct_pairs(*pairs: Iterable[str]) -> List[Tuple[Path, Path]]:
    return [
        (Path(path1), Path(path2)) for path1, path2 in pairs
    ]
