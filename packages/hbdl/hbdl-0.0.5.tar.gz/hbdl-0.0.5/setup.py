# -*-coding: utf-8-*-
import io
import pathlib

import setuptools

README = (pathlib.Path(__file__).parent / "README.md").read_text()

REQUIRES = [
    dep_line
    for line in io.StringIO((pathlib.Path(__file__).parent / "requirements.txt").read_text())
    if (dep_line := line.strip())
]

setuptools.setup(
    name="hbdl",
    version="0.0.5",
    author="unkloud",
    author_email="unkloud.com.au@gmail.com",
    description="Another humble bundle downloader",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/unkloud/hbdl.git",
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    entry_points={"console_scripts": ["hbdl=hbdl.hbdl:download"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
