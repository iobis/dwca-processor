from setuptools import setup

setup(
    name="dwcaprocessor",
    description="Process DwCA",
    author="Pieter Provoost",
    author_email="pieterprovoost@gmail.com",
    version="0.1.0",
    packages=["dwcaprocessor"],
    dependency_links=["https://github.com/pieterprovoost/csvreader/tarball/master#egg=csvreader-0.2.0"],
    install_requires="csvreader"
)