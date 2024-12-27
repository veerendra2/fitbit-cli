# -*- coding: utf-8 -*-
"""
setup.py
"""
# pylint: disable=C0301

import re

from setuptools import find_packages, setup

with open("fitbit_cli/__init__.py", encoding="utf-8") as file:
    REGEX_VERSION = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(REGEX_VERSION, file.read(), re.MULTILINE).group(1)  # type: ignore[union-attr]

with open("README.md", encoding="utf-8") as file:
    readme = file.read()

setup(
    name="fitbit-cli",
    version=version,
    packages=find_packages(),
    description="Access your Fitbit data at your terminal.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="veerendra2",
    author_email="vk.tyk23@simplelogin.com",
    url="https://github.com/veerendra2/fitbit-cli",
    download_url=f"https://github.com/veerendra2/fitbit-cli/archive/{version}.tar.gz",
    project_urls={
        "Documentation": "https://github.com/veerendra2/fitbit-cli",
    },
    keywords=["fitbit", "fitbit-api", "cli", "python"],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
    install_requires=[
        "requests==2.32.3",
        "rich==13.9.4",
    ],
    python_requires=">=3.9",
    entry_points={"console_scripts": ["fitbit-cli = fitbit_cli.main:main"]},
)
