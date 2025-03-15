import os
from setuptools import setup
from Cython.Build import cythonize

# Define the source files
source_files = ["bindings/example.pyx", "bindings/tuning_utils.pyx"]

# Define the output directory (one level above)
output_dir = os.path.dirname(os.getcwd())

setup(
    ext_modules=cythonize(source_files, language_level=3),
    package_dir={"": output_dir},  # Set base package directory
)
