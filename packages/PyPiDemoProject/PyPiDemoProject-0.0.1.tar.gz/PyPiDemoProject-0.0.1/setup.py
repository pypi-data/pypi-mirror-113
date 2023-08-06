#!/usr/bin/env python
from __future__ import print_function
import setuptools
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PyPiDemoProject",
    version = "0.0.1",
    author = "author",
    author_email = "author@example.com",
    description = "PyPI Demo Project",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license = "MIT",
    url = "https://github.com/muyinliu/PyPiDemoProject",
    package_dir={"": "src"},
    packages=["example_package", "example_package.utils"],
    install_requires = [
      "wheel==0.36.2"
    ],
    classifiers = [
      "Environment :: Web Environment",
      "Intended Audience :: Developers",
      "Operating System :: OS Independent",
      "Topic :: Text Processing :: Indexing",
      "Topic :: Utilities",
      "Topic :: Internet",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6"
)