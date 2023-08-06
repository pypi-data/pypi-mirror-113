#!/usr/bin/env python
import setuptools

from pathlib import Path
from distutils.core import setup

README = Path(__file__).parent / "README.md"
with open(README, "r") as fp:
    long_description = fp.read()

setup(
    name='ATRFileHandler',
    version='0.1.1',
    description='Time handler for repetitive short-duration processes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Manuel Pepe',
    author_email='manuelpepe-dev@outlook.com.ar',
    url = 'https://github.com/manuelpepe/ATRFileHandler',
    include_package_data=True,
    packages=[
        'ATRFileHandler',
    ],
)
