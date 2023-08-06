#!/usr/bin/python

import os
from glob import glob

from setuptools import find_packages, setup

from translation_comparator import __name__, __version__

requirements = {}
for path in glob("requirements/*.txt"):
    with open(path) as file:
        name = os.path.basename(path)[:-4]
        requirements[name] = [line.strip() for line in file]

with open("README.md") as file:
    long_description = file.read()

setup(
    name=__name__,
    version=__version__,
    description="Helps to compare translated code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="0dminnimda",
    author_email="0dminnimda.contact@gmail.com",
    packages=find_packages(),
    license="MIT",
    install_requires=requirements.pop("basic"),
    python_requires=">=3.7",
    extras_require=requirements
)
