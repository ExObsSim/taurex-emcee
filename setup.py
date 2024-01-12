#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

packages = find_packages(exclude=("tests", "doc"))
provides = [
    "taurex_emcee",
]

requires = []

install_requires = [
    "taurex",
    "emcee",
    "corner",
    "arviz",
]

entry_points = {"taurex.plugins": "emcee = taurex_emcee"}

with open("README.md", "r") as fh:
    long_description = fh.read()

version = "0.4.0-alpha"

setup(
    name="taurex_emcee",
    author="Andrea Bocchieri",
    author_email="andrea.bocchieri@uniroma1.it",
    license="BSD",
    description="emcee plugin for TauREx-3 ",
    packages=packages,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points=entry_points,
    version=version,
    keywords=[
        "exoplanet",
        "emcee",
        "sampling",
        "ensemble sampling",
        "taurex",
        "chemistry",
        "plugin",
        "taurex3",
        "atmosphere",
        "atmospheric",
    ],
    provides=provides,
    requires=requires,
    install_requires=install_requires,
)
