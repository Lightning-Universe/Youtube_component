#!/usr/bin/env python

from setuptools import find_packages, setup

with open("requirements.txt") as _file:
    install_reqs = [req for req in _file.readlines()]

with open("tests/requirements.txt") as _file:
    test_reqs = [req for req in _file.readlines()]

setup(
    name="lai_youtubedownloader",
    version="0.0.1",
    description="Component used to fetch youtube videos",
    author="Eric Chea",
    author_email="eric@lightning.ai",
    url="https://github.com/Lightning-AI/LAI-youtube-Component",
    install_requires=install_reqs,
    packages=find_packages(),
    extras_require={
        "test": test_reqs,
    },
)
