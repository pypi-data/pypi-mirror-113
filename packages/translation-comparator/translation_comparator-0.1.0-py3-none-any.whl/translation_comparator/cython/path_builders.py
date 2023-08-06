#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Tuple


def build_via_suffix_change(path: Path) -> Tuple[Path, Path]:
    "'path.*' -> 'path.py', 'path.pyx'"
    return path.with_suffix(".py"), path.with_suffix(".pyx")


def unique_stem_via_suffix(path: Path) -> Path:
    return path.with_stem(path.stem + "_" + path.suffix[1:])


def unique_name_via_number(path: Path) -> Tuple[Path, Path]:
    return (path.with_name(path.name + " (0)"),
            path.with_name(path.name + " (1)"))
