from setuptools import setup, find_packages
from tdfs import __version__

NAME = "tdfs"

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name=NAME,
    version=__version__,
    description="Feature Store frontend using Teradata Dataframes",
    python_requires='>=3.6.0',
    author="Teradata",
    author_email="teradata.corporation@teradatacorporation.com",
    url="",
    install_requires=required,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True
)
