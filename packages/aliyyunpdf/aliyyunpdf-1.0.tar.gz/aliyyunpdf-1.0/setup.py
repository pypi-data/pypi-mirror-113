import setuptools
from pathlib import Path
setuptools.setup(
    name="aliyyunpdf",
    version=1.0,
    long_decription=Path("README.md").read_text(),
    # picking the ones to exclude when finding the packages to place
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
