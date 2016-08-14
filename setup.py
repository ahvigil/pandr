import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pandr",
    version = "0.1.0",
    author = "Arthur Vigil",
    author_email = "me@ahv.io",
    description = ("R compatible pandas dataframe serialization."),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license = "MIT",
    packages=['pandr']
)
