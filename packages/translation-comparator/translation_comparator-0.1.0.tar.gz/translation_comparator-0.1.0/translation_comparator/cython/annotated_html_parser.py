#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from typing import List, Tuple

from bs4 import BeautifulSoup, FeatureNotFound
from bs4.element import Tag


def get_code_from_soup(soup: BeautifulSoup) -> List[str]:
    return [
        tag.text for tag in soup.find_all("pre", class_="code")]


def get_soup_from_html(path: Path) -> BeautifulSoup:
    html = path.with_suffix(".html").read_text()

    html = html.replace(path.stem, "{fname}")
    html = html.replace(path.stem[:-1], "{fname}")
    html = re.sub(r"\d+{fname}", "{num_fname}", html)
    html = html.replace("{fname}" + "_" + path.suffix[1:],
                        "{fname_suf}")

    try:
        return BeautifulSoup(html, "lxml")
    except FeatureNotFound:
        try:
            return BeautifulSoup(html, "html5lib")
        except FeatureNotFound:
            return BeautifulSoup(html, "html.parser")


def get_code_from_two_files_by_path(
    path1: Path, path2: Path
) -> Tuple[List[str], List[str]]:

    return (
        get_code_from_soup(get_soup_from_html(path1)),
        get_code_from_soup(get_soup_from_html(path2)))


def get_code_from_two_files(
    file1: str, file2: str
) -> Tuple[List[str], List[str]]:

    return get_code_from_two_files_by_path(
        Path(file1), Path(file2))
