#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from difflib import Differ
from pathlib import Path
from typing import Container

from ..show_functions import show_via_cmd
from ..typedefs import GEN_PATH_FUNC, PATH_FUNC, SHOW_FUNC
from .path_builders import (build_via_suffix_change, unique_name_via_number,
                            unique_stem_via_suffix)

replace_threshold: int = 3
str_between_lines: str = "\n  " + "#"*100 + "\n  "*2

out_ext: str = ".txt"
diff_ext: str = ".diff"
extensions: Container[str] = (".py", ".pyx")

build_dir: Path = Path("build/")
py_dir: Path = Path("py/")
pyx_dir: Path = Path("pyx/")
diff_dir: Path = Path("diff/")

path_func: GEN_PATH_FUNC = build_via_suffix_change
show_func: SHOW_FUNC = show_via_cmd
unique_stem_func: PATH_FUNC = unique_stem_via_suffix
unique_name_func: GEN_PATH_FUNC = unique_name_via_number

save_as_diff: bool = True
create_dirs: bool = True

differ: Differ = Differ()
