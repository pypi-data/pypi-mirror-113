from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(name = "Cdatatype",
version = "1.0.1",
description = "A python package to count datatypes and null values in columns",
long_description = readme(),
long_description_content_type = "text/markdown",
author = "Thiru Siddharth",
author_email = "thirusid789@gmail.com",
packages = ['Cdatatype'],
license = "MIT",
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8"
],
include_package_data = True,
install_requires = ['pandas'])