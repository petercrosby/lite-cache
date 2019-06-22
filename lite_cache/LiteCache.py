"""
Key-value storage with optional persistence for Python3 programs using SQLite3.

lite_cache/LiteCache.py
"""

import os
import sys
import json
import shutil
import logging

from sqlite3 import Connection, IntegrityError


DEFAULT_CACHE_NAME = 'litecache'
DEFAULT_CACHE_DIRECTORY = os.path.join(os.path.expanduser('~'), '.local', DEFAULT_CACHE_NAME)
DISABLE_PERSISTENT_CACHING = False


class LiteCache:
    """
    LiteCache
    """
    _CREATE_SQL = (
        "CREATE TABLE IF NOT EXISTS entries ( key TEXT PRIMARY KEY, val BLOB )"
    )
    _CREATE_INDEX = "CREATE INDEX IF NOT EXISTS keyname_index ON entries (key)"
    _GET_SQL = "SELECT val FROM entries WHERE key = ?"
    _DUMP_SQL = "SELECT * from entries"
    _DEL_SQL = "DELETE FROM entries WHERE key = ?"
    _SET_SQL = "REPLACE INTO entries (key, val) VALUES (?, ?)"
    _ADD_SQL = "INSERT INTO entries (key, val) VALUES (?, ?)"
    _CLEAR_SQL = "DELETE FROM entries"

    cache_db = None
    connection = None

    cache_directory = DEFAULT_CACHE_DIRECTORY
    cache_name = DEFAULT_CACHE_NAME

    def __init__(self, cache_directory: str = DEFAULT_CACHE_DIRECTORY, cache_name: str = DEFAULT_CACHE_NAME):
        """

        Args:
            cache_directory: str - Optional
            cache_name: str - Optional

        """
        if not cache_directory:
            cache_directory = DEFAULT_CACHE_DIRECTORY

        if not os.path.isdir(cache_directory):
            try:
                # Create the directory
                os.mkdir(cache_directory)

            except OSError as e:
                logging.exception(e)
                raise

        if not cache_name:
            cache_name = DEFAULT_CACHE_NAME

        named_cache_directory = os.path.join(cache_directory, cache_name)

        # Check if the directory exists
        if not os.path.isdir(named_cache_directory):
            try:
                # Create the directory
                os.mkdir(named_cache_directory)

            except OSError as e:
                logging.exception(e)
                raise

        self.cache_directory = named_cache_directory
        self.cache_name = cache_name
        self.cache_db = os.path.join(self.cache_directory, '{}.db'.format(self.cache_name))

        # Check if the directory exists
        if not os.path.isdir(self.cache_directory):
            try:
                # Create the directory
                os.mkdir(self.cache_directory)

            except OSError as e:
                logging.exception(e)
                raise

    def flush(self) -> bool:
        """
        Flush the database tables.

        Returns:
            bool:
        """
        with self._get_conn() as conn:
            try:
                conn.execute(self._CLEAR_SQL)
                logging.debug('Cache Flushed')
                return True

            except IntegrityError as e:
                logging.exception(e)
                raise

    def _get_conn(self) -> Connection:
        """
        Returns the Cache connection.

        Returns:
            Connection:
        """
        if self.connection:
            return self.connection

        conn = Connection(self.cache_db)

        with conn:
            conn.execute(self._create_sql)
            conn.execute(self._create_index)
            logging.debug('Ran the create table && index SQL.')

        # set the connection property
        self.connection = conn

        # return the connection
        return self.connection

    def get(self, key) -> str:
        """
        Retrieve a value from the cache.

        Args:
            key: str - name of the value to fetch

        Returns:
            str:
        """
        assert key, 'key cannot be blank'
        assert isinstance(key, str), 'key must be a string'

        return_value = None
        # get a connection to run the lookup query with
        with self._get_conn() as conn:
            # loop the response rows looking for a result
            for row in conn.execute(self._get_sql, (key,)):
                return_value = json.loads(row[0])
                break

        return return_value

    def delete(self, key: str):
        """
        Delete a cache entry.

        Args:
            key: str -

        Returns:

        """
        assert key, 'key cannot be blank'
        assert isinstance(key, str), 'key must be a string'

        with self._get_conn() as conn:
            conn.execute(self._del_sql, (key,))

    def update(self, key: str, value):
        """
        Sets a key, value pair.

        Args:
            key: str -
            value: str or dict -

        Returns:

        """
        assert key, 'key cannot be blank'
        assert isinstance(key, str), 'key must be a string'
        assert value, 'value cannot be blank'

        data = json.dumps(value)

        # write the updated value to the db
        with self._get_conn() as conn:
            conn.execute(self._set_sql, (key, data))

    def set(self, key: str, value):
        """
        Adds a k,v pair.

        Args:
            key: str -
            value: str or dict -

        Returns:

        """
        assert key, 'key cannot be blank'
        assert isinstance(key, str), 'key must be a string'
        assert value, 'value cannot be blank'

        data = json.dumps(value)

        with self._get_conn() as conn:
            try:
                conn.execute(self._add_sql, (key, data))
            except IntegrityError as e:
                logging.debug(e)
                self.update(key, value)

    def dump(self) -> list:
        """
        Dump the cache to a list.

        Returns:
            list:
        """
        res = []
        with self._get_conn() as conn:
            for row in conn.execute(self._dump_sql,):
                res.append(row)
        return res

    def clear(self):
        """
        Clear a cache.

        Returns:

        """
        with self._get_conn() as conn:
            conn.execute(self._clear_sql,)

    def __del__(self):
        """
        Cleans up the object by destroying the sqlite connection.

        Returns:

        """
        if self.connection:
            self.connection.close()

    def cleanup_app(self) -> bool:
        """
        Remove the cache database files and directory.

        Returns:
            bool:
        """
        if not os.path.isdir(self.cache_dir):
            return False

        try:
            shutil.rmtree(self.cache_dir)
        except OSError as e:
            logging.exception(e)
            return False
        else:
            return True