"""
lite-cache
----------
Simple key-value cache for Python3 using SQLite3.

Referenced from: http://flask.pocoo.org/snippets/87/

Links
`````
* `Docs <https://github.com/petercrosby/lite-cache>`_
* `SQLite Cache <http://flask.pocoo.org/snippets/87/>`_
* `GitHub <https://github.com/petercrosby/lite-cache>`_

"""

import os
import sys
import re

from setuptools import setup, find_packages
from setuptools.command.install import install


NAME = "lite-cache"
project_url = "https://github.com/petercrosby/lite-cache"
description = "Simple key-value cache for Python3 using SQLite3."
keywords = ("python sqlite3 cache json setuptools")


with open(os.path.join("lite_cache", "__init__.py"), "rt") as f:
    version = re.search("__version__ = \"([^\"]+)\"", f.read()).group(1)

if sys.version_info < (3, 6, 0):
    print('ERROR: {} requires at least Python 3.6.0 to run.'.format(NAME))
    sys.exit(1)

# Set the requirements.txt file path, located next to setup.py
requirements_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'requirements.txt')


def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version
            )
            sys.exit(info)


try:
    with open(requirements_file, 'r') as open_file:
        requirements = open_file.readlines()
except (FileNotFoundError, IOError):
    raise

setup(
    name=NAME,
    version=version,
    description=description,
    long_description=readme(),
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
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
    python_requires='>=3.6.0',
    platforms=["linux", "linux2", "darwin"],
    packages=find_packages(exclude=("tests", "setup")),
    test_suite="tests",
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
