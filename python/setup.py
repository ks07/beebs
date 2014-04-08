import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "beebs",
    version = "0.1dev1",
    author = "James Pallister",
    author_email = "james.pallister@bristol.ac.uk",
    description = ("Module to interact with BEEBS"),
    license = "LGPL",
    keywords = "energy benchmark BEEBS MAGEEC",
    # url = "http://packages.python.org/an_example_pypi_project",
    package_dir={'':'src'},
    packages=['beebs'],
    long_description=read('README.rst'),
    install_requires=['docopt>=0.6.1', 'pexpect>=3.1'],
    zip_safe=True
)
