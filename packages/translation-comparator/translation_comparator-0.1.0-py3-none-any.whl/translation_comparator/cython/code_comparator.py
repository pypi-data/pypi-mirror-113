#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from difflib import restore
from pathlib import Path
from re import Match
from typing import Iterable, List

from ..path_helpers import change_same_paths_if_needed
from ..typedefs import DIFF, DIFF_FUNC, DIFF_ITER
from . import settings
from .annotated_html_parser import get_code_from_two_files_by_path


def diff_to_str(diff: DIFF) -> str:
    return settings.str_between_lines.join(["\n".join(i) for i in diff])


def make_diff(func: DIFF_FUNC, iterable: DIFF_ITER) -> DIFF:
    return [
        list(func(a.split("\n"), b.split("\n")))
        for a, b in iterable]


def write_restored_diff(path: Path, lines: Iterable[str]) -> None:
    build_out_path(path).write_text("\n".join(lines))


def repl(match: Match) -> str:
    if (
        0 < match.group(2).count("^") < settings.replace_threshold and
        0 < match.group(4).count("^") < settings.replace_threshold
    ):
        return f"  {match.group(1)}"

    return match.group(0)


def equate_similar_lines(string: str) -> str:
    pattern = re.compile(r"- (.+)\n\? (.+)\n\n\+ (.+)\n\? (.+)")

    return pattern.sub(repl, string)


def build_diff_path(path1: Path, path2: Path) -> Path:
    return settings.diff_dir.joinpath(
        path1.stem + "+" + path2.stem).with_suffix(settings.diff_ext)


def build_out_path(path: Path) -> Path:
    return settings.diff_dir.joinpath(  # ..path_helpers.full_path
        path.name).with_suffix(settings.out_ext)


def compare_and_save_two_files_by_path(path1: Path, path2: Path) -> None:
    code1, code2 = get_code_from_two_files_by_path(path1, path2)

    compare_result = make_diff(settings.differ.compare, zip(code1, code2))
    comparison_str = equate_similar_lines(diff_to_str(compare_result))

    path1, path2 = change_same_paths_if_needed(path1, path2)
    if settings.save_as_diff:
        build_diff_path(path1, path2).write_text(comparison_str)
    else:
        split = comparison_str.split("\n")
        write_restored_diff(path1, restore(split, 1))
        write_restored_diff(path2, restore(split, 2))


def compare_and_save_two_files(file1: str, file2: str) -> None:
    return compare_and_save_two_files_by_path(Path(file1), Path(file2))
