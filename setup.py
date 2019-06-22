"""
jsonlite-cache
----------
Simple key-value cache for Python3 using SQLite3.

Referenced from: http://flask.pocoo.org/snippets/87/

Links
`````
* `Docs <https://github.com/petercrosby/jsonlite-cache>`_
* `SQLite Cache <http://flask.pocoo.org/snippets/87/>`_
* `GitHub <https://github.com/petercrosby/jsonlite-cache>`_

"""

import os
import sys
import re

from setuptools import setup, find_packages


NAME = "jsonlite-cache"
project_url = "https://github.com/petercrosby/jsonlite-cache"
description = "Simple key-value cache for Python3 using SQLite3."
keywords = ("python sqlite3 cache json setuptools")


with open(os.path.join("jsonlite_cache", "__init__.py"), "rt") as f:
    version = re.search("__version__ = \"([^\"]+)\"", f.read()).group(1)

if sys.version_info < (3, 5, 2):
    print('ERROR: {} requires at least Python 3.5.2 to run.'.format(NAME))
    sys.exit(1)

# Set the requirements.txt file path, located next to setup.py
requirements_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'requirements.txt')

try:
    with open(requirements_file, 'r') as open_file:
        requirements = open_file.readlines()
except (FileNotFoundError, IOError):
    raise

setup(
    name=NAME,
    version=version,
    description=description,
    long_description=__doc__,
    author="Peter Crosby",
    author_email="p.crosby25@gmail.com",
    maintainer="p.crosby25@gmail.com",
    license="GPLv3",
    url=project_url,
    keywords=keywords,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: SQL",
        "Natural Language :: English",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=requirements,
    python_requires='>=3.5.2',
    platforms=["linux", "linux2", "darwin"],
    packages=find_packages(exclude=("tests", "setup")),
    test_suite="tests"
)
