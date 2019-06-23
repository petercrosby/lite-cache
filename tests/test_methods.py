#!/usr/bin/env python3

import logging
import unittest

from lite_cache.cache import cache
from tests.mock import random_str, random_data


class TestCacheMethods(unittest.TestCase):
    def test_method_props(self):
        methods = ['set', 'get', 'update', 'delete', 'dump', 'flush', 'cleanup']

        for method in methods:
            # Ensure is an attribute
            self.assertTrue(hasattr(cache, method))

            # Ensure attribute is callable
            self.assertTrue(callable(getattr(cache, method)))

    def test_method_calls(self):
        # Random key
        key = random_str(16)
        # Random data
        data = str(random_data())

        # # Run test routine
        # # Ensure key is not already in cache
        # cached_data = cache.get(key)
        # self.assertIsNone(cached_data)
        #
        # # Add the data to the cache at the key
        # cache.set(key, str(data))
        #
        # # Check key is in cache
        # self.assertEquals(str(data), cache.get(key))

        # Check cache size

        # Remove the data at the key

        # Check key is no longer in cache

        # Check cache size

        # Check other keys still exist in cache


if __name__ == "__main__":
    # disable logging
    logging.basicConfig(level=logging.INFO)

    # run tests
    unittest.main()
