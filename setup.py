from setuptools import setup, find_packages

setup(
    name="bjpaoc",
    version="0.1",
    description="bjp's solutions for https://adventofcode.com/",
    url="https://github.com/bj0/aoc",
    author="Brian Parma",
    author_email="execrable@gmail.com",
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
        "advent-of-code-data >= 0.8.0",
        "networkx",
        "trio"
        # list your other requirements here, for example:
        # "numpy", "parse", "networkx",
    ],
    packages=find_packages(),
    entry_points={"adventofcode.user": ["bjp = aoc:solve"]},
)
