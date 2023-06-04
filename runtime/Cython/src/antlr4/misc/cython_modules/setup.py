from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("MurmurHash.pyx", language_level = "3"),
    package_dir = { "antlr4/misc" : "" }
)