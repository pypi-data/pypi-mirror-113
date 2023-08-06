from distutils.core import setup
from setuptools import find_packages, setup

import numpy
from Cython.Build import cythonize

with open("README.md", 'r') as f:
    long_description = f.read()

#fileSet = set()
#fileSet.add("./computations_library/__init__.pyx")

setup(name="computations_library",
    zip_safe=False,
    version="1.1.1",
    packages=find_packages(),
    author="Mohit Sharma",
    description="A classification library used to compute ravi strategy for now",
    long_description=long_description,
    install_requires=['numpy>=1.18.1','Cython>=0.29.22'],
    ext_modules = cythonize('./computations_library/__init__.pyx'),include_dirs=[numpy.get_include()])
