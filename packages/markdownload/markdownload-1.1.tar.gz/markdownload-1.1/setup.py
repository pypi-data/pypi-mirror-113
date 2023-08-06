import setuptools
from pathlib import Path

setuptools.setup(
    name="markdownload",
    version=1.1,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
