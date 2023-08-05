"""
 Copyright (c) 2021 Faisal Thaheem (https://github.com/faisalthaheem/python-stanag-4586-EDA-v1)
 License GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
"""

import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='stanag4586vsm',
    packages=find_packages(include=['stanag4586vsm']),
    version='0.0.7',
    description='Python Stanag 4586 VSM implementation',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/faisalthaheem/python-stanag-4586-vsm",
    author='Faisal Thaheem',
    license='GPLV3',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)