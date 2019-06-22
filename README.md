# jsonlite-cache
[![PyPi version](https://pypip.in/v/py-cache/badge.png)](https://github.com/petercrosby/jsonlite_cache/blob/master/LICENSE)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/py-cache.svg?style=flat)](https://pypi.python.org/pypi/web_cache/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/petercrosby/jsonlite_cache/blob/master/LICENSE)

Simple sqlite key-value storage for Python3.

Python3 module for caching data during a program's runtime, with optional persistence.

## Features

* Program specific cache files.
* Simple encoding of data using standard `json` package.
* Optional persistence of data across multiple executions.
    - Useful for keeping some runtime data available to a program after a full exit.
        - ex. `raise Exception` or `sys.exit()`, etc 

## Installation (from PyPI, with PIP)

`jsonlite-cache` requires [Python](https://www.python.org/downloads/) >= 3.5.

1. If not already installed, [install pip](https://pip.pypa.io/en/stable/installing/) for Python 3
2. Install `jsonlite_cache`
    ```bash
    $ pip3 install jsonlite-cache
    ````

### Usage
```python
import jsonlite_cache

# Create a new instance
lite_cache = jsonlite_cache.LiteCache()



```

```python
from jsonlite_cache import LiteCache

# Set the client

```
## Development
This project uses `pipenv` for managing virtual-environments and Python3 dependencies  for development and testing.
* **Reference**: https://pypi.org/project/pipenv/

The standard `requirements.txt` is included for installation via `setup.py`

## Plans
- Interface for handling Python+Sqlite3 thread limitations.
- Data compression options


## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
