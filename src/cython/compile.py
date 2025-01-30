import os
from setuptools import setup
from Cython.Build import cythonize

# Define the source file
source_file = "src/cython/example.pyx"

# Define the output directory (one level above)
output_dir = os.path.dirname(os.getcwd())

setup(
    ext_modules=cythonize(source_file),
    package_dir={"": output_dir},  # Set base package directory
)
