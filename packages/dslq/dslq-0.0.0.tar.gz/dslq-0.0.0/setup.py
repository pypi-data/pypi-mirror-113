from sys import version
from setuptools import setup, find_packages

with open("README.md") as _readme:
    readme = _readme.read()

setup(
    name = "dslq",
    author = "Mrinal Sinha",
    author_email = "mail@themrinalsinha.com",
    python_requires = ">=3.6, <4",
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description = "",
    long_description = readme,
    long_description_content_type = "text/markdown",
    include_package_data = True,
    packages = find_packages(include=["dslq", "dslq.*"]),
    url = "https://github.com/themrinalsinha/dslq",
    version = "0.0.0",
    zip_safe = False,
    # install_requires = []
)
