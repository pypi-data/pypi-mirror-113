from setuptools import find_packages, setup
# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work

setup(
    name='mypythonlibpooja',
    packages=find_packages(include=['mypythonlib']),
    version='0.1.0',
    description='My first Python library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mypythonlibpooja.readthedocs.io/",
    author='Me',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner','numpy'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)