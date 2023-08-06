from os import name
from setuptools import setup, find_packages

setup(
    name="scanfs",
    version="0.0.1",
    description="File system scanner in Python",
    author="CPU Info",
    author_email="cpuinfo10@gmail.com",
    extra_requires=dict(tests=["pytest"]),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/cpuinfo/scanfs",
)
