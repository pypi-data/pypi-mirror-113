#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import warnings

from .typedefs import SHOW_FUNC_DATA


def show_via_vscode(save_as_diff: bool, data: SHOW_FUNC_DATA) -> None:
    if save_as_diff:
        os.system(f"code {data[0]}")  # open file in vscode
    else:
        os.system(f"code --diff {data[0]} {data[1]}")  # open file diff


def show_via_cmd(save_as_diff: bool, data: SHOW_FUNC_DATA) -> None:
    if sys.platform == "win32":
        if save_as_diff:
            os.system(f"more \"{data[0]}\"")  # output file contents
        else:
            os.system(f"FC \"{data[0]}\" \"{data[1]}\"")  # output file diff
    elif (sys.platform.startswith('linux') or
          sys.platform in ('cygwin', 'darwin')
    ):
        if save_as_diff:
            os.system(f"cat \"{data[0]}\"")  # open file contents
        else:
            os.system(f"diff \"{data[0]}\" \"{data[1]}\"")  # output file diff
    else:
        warnings.warn("Viewing cmd difference is not yet supported in " +
                      sys.platform + " (" + os.name + ")")
