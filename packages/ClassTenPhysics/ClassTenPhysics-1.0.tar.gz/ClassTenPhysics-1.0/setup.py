import setuptools
from pathlib import Path

from setuptools import version
setuptools.setup(
    name="ClassTenPhysics",
    version=1.0,
    long_description=Path("README.rst").read_text(),
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=["tests"])
)
