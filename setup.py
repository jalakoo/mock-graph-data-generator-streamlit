# Run `pipenv install -e . --dev` at least once so that pytest can import all files for testing
from setuptools import find_packages, setup

setup(
    name="mock_generators",
    package_dir={'': 'mock_generators'},
    packages=find_packages(where='mock_generators'),
)