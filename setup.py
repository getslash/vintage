import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "vintage", "__version__.py")) as version_file:
    exec(version_file.read()) # pylint: disable=W0122

_INSTALL_REQUIERS = [
    'six',
]

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(name="vintage",
      classifiers = [
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          ],
      description="Python library for deprecating code",
      long_description=long_description,
      long_description_content_type='text/markdown',
      license="BSD3",
      author="Slash Developers",
      author_email="vmalloc@gmail.com",
      version=__version__, # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),

      url="https://github.com/getslash/vintage",

      install_requires=_INSTALL_REQUIERS,
      scripts=[],
      namespace_packages=[]
      )
