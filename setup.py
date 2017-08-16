from setuptools import setup

setup(
    name="dwcaprocessor",
    description="Process DwCA",
    author="Pieter Provoost",
    author_email="pieterprovoost@gmail.com",
    version="0.0.2",
    packages=["dwcaprocessor"],
    dependency_links=["https://github.com/pieterprovoost/csvreader/tarball/master"],
    install_requires="csvreader"
)