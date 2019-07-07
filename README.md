# lite-cache
[![PyPi version](https://pypip.in/v/py-cache/badge.png)](https://github.com/petercrosby/lite-cache/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/petercrosby/lite-cache/branch/develop/graph/badge.svg)](https://codecov.io/gh/petercrosby/lite-cache)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/lite-cache.svg?style=flat)](https://pypi.python.org/pypi/web_cache/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/petercrosby/lite-cache/blob/master/LICENSE)

| Branch| Build Status  |
| --- | --- |
|`master`| [![CircleCI](https://circleci.com/gh/petercrosby/lite-cache/tree/master.svg?style=svg)](https://circleci.com/gh/petercrosby/lite-cache/tree/master)|
|`develop`| [![CircleCI](https://circleci.com/gh/petercrosby/lite-cache/tree/develop.svg?style=svg)](https://circleci.com/gh/petercrosby/lite-cache/tree/develop)|

Simple sqlite key-value storage for Python3.

Python3 module for caching data during a program's runtime, with optional persistence.

## Features

* Program specific cache.
* Simple encoding of data using standard `json` package.
* Optional persistence of data across multiple executions.
    - Useful for keeping some runtime data available to a program after a full exit.
        - ex. `raise Exception` or `sys.exit()`, etc

## Installation (from PyPI, with PIP)

`lite-cache` requires [Python](https://www.python.org/downloads/) >= 3.6.

1. If not already installed, [install pip](https://pip.pypa.io/en/stable/installing/) for Python 3
2. Install `lite_cache`
    ```bash
    $ pip3 install lite-cache
    ````

### Usage

To use in default configuration:
- Entire cache is in 1 database file, `~/.local/litecache/cache.db`

To use in custom configuration:

```Python3
import lite_cache

program_cache = lite_cache.LiteCache(name='MyProgramCache', location='~/.local/litecache')
# This initializes and creates a new Sqlite3 database file in `location` directory,
# named as "`name`.cache".
# If directory does not exist, error is raised.

```

This strategy of having unique caches for each program is designed to navigate "same thread" or "single thread" issues with Python & Sqlite3.
- This would not prevent issues occurring if multiple instances of the same program were launched on the same machine.
  - ie. Executing same Python script in 2 terminal tabs. This would lead to two(2) threads attempting to access one(1) Sqlite3 with same `name`


## Development
This project uses `pipenv` for managing virtual-environments and Python3 dependencies  for development and testing.
* **Reference**: https://pypi.org/project/pipenv/

The standard `requirements.txt` is included for installation via `setup.py`

## Tests
- Uses `unittests`

Run all tests from `setup.py`
```bash
pipenv run python setup.py test
```

Run specific test
```bash
pipenv run python -m unittest tests/test_main.py
```

## Plans
- Interface for handling Python+Sqlite3 thread limitations.
- Data compression options


## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
