#!/usr/bin/env python3

import collections
import gc
import logging
import os
import pickle
import random
import string
import sys
import tempfile
import time
import unittest

import lite_cache


def random_name():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


class TestWebCache(unittest.TestCase):
    def test_init_default_cache(self):
        # Init a cache with default settings
        cache = lite_cache.LiteCache()
        print(cache)

    def test_init_custom_cache(self):
        # random_name = random_name()
        cache = lite_cache.LiteCache()
        print(cache)


if __name__ == "__main__":
    # disable logging
    logging.basicConfig(level=logging.INFO)

    # run tests
    unittest.main()
