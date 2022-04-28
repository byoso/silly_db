#! /usr/bin/env python3
# coding: utf-8

"""
1- build
./setup.py sdist bdist_wheel
2- basic verifications
twine check dist/*
3- upload to PyPi
twine upload dist/*
"""


import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="silly_db",
    version="1.0.0",
    description=(
        "Python3 tool to create and handle very quickly a sqlite3 "
        "database in an application"
        ),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/byoso/silly_db",
    author="Vincent Fabre",
    author_email="peigne.plume@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    packages=["silly_db"],
    include_package_data=True,
    # install_requires=[],
    entry_points={
        "console_scripts": [
            "realpython=flamewok.__main__:main",
        ]
    },
    setup_requires=['wheel'],
)
