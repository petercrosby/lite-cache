#!/usr/bin/env python3

import logging
import unittest

import lite_cache
from tests.mock import random_str, random_data


class TestDefault(unittest.TestCase):
    def test_default(self):
        # Init cache client
        litecache = lite_cache.LiteCache(cache_name='test_default', persist=True)

        # Random key
        key = random_str(16)
        # Random data
        data = random_data()

        # Run test routine
        # Ensure key is not already in cache
        cached_data = litecache.get(key)
        self.assertIsNone(cached_data)

        # Add the data to the cache at the key
        litecache.set(key, str(data))

        # Check key is in cache
        self.assertEqual(str(data), litecache.get(key))


if __name__ == "__main__":
    # disable logging
    logging.basicConfig(level=logging.INFO)

    # run tests
    unittest.main()
