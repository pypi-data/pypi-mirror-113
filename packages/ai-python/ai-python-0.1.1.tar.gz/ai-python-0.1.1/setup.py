# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import io
import os

# NOTE: DO NOT change the import order, as sometimes there is a conflict between setuptools and distutils,
# it will cause following error:
# error: each element of 'ext_modules' option must be an Extension instance or 2-tuple
from setuptools import find_packages
from distutils.core import setup

readme = io.open("./README.md", encoding="utf-8").read()

setuptools = "setuptools>=54.2.0,<=54.2.0"

core_requires = io.open("./requirements.txt", encoding="utf-8").read()

test_requires = io.open("./test/requirements.txt", encoding="utf-8").read()

extras = {
    "required": [],
    "core": core_requires,
    "test": test_requires,
}

SETUP_REQUIRES = [
    "jupyter-packaging==0.7.12",
    "numpy==1.19.5",
    "pip-tools==5.5.0",
    "scikit-build==0.11.1",
    "scipy==1.4.1",
]


setup(
    name="ai-python",
    version="0.1.1",
    description="Microsoft AI Python Package",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Daniel Ciborowski",
    author_email="dciborow@microsoft.com",
    url="https://github.com/microsoft/ai-python",
    project_urls={
        "Code": "https://github.com/microsoft/ai-python",
        "Issues": "https://github.com/microsoft/ai-python/issues",
        "Documents": "https://github.com/microsoft/ai-python"
    },
    license="MIT License",
    platforms=["Windows", "Linux", "macOS"],
    keywords=["ai"],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"],
    python_requires=">=3.7,<3.8",
    setup_requires=SETUP_REQUIRES,
    extras_require=extras,
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    include_package_data=True,
    zip_safe=False,
)
