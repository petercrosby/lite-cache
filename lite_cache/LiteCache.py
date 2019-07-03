"""
Key-value storage with optional persistence for Python3 programs using SQLite3.

lite_cache/LiteCache.py
"""

import os
import json
import shutil
import logging

from sqlite3 import Connection, IntegrityError


DEFAULT_CACHE_DIRECTORY = os.path.join(os.path.expanduser('~'), '.local', 'litecache')


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
    cache_name = None
    cache_directory = DEFAULT_CACHE_DIRECTORY
    persist = False

    def __init__(self, cache_name: str = '', cache_dir: str = DEFAULT_CACHE_DIRECTORY, persist: bool = False):
        """

        Args:
            cache_name: str - Required
            cache_dir: str - Optional
            persist: bool - Optional

        """
        assert cache_dir, 'cache_dir cannot be blank'
        assert isinstance(cache_dir, str), 'cache_dir must be a string'

        assert cache_name, 'cache_name cannot be blank'
        assert isinstance(cache_name, str), 'cache_name must be a string'

        assert isinstance(persist, bool), 'persist must be a boolean'

        # Ensure the cache directory exists
        if not os.path.isdir(cache_dir):
            try:
                # Create the directory
                os.mkdir(cache_dir)

            except OSError as e:
                logging.exception(e)
                raise

        # Check if the directory exists
        if not os.path.isdir(cache_dir):
            try:
                # Create the directory
                os.mkdir(cache_dir)

            except OSError as e:
                logging.exception(e)
                raise

        self.cache_directory = cache_dir
        self.cache_name = cache_name
        self.cache_db = os.path.join(self.cache_directory, '{}.db'.format(self.cache_name))
        self.persist = persist

        # Check if a cache db already exists
        # if it does and persist=False, then cleanup
        if not self.persist:
            self.cleanup()

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
            conn.execute(self._CREATE_SQL)
            conn.execute(self._CREATE_INDEX)
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
            for row in conn.execute(self._GET_SQL, (key,)):
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
            conn.execute(self._DEL_SQL, (key,))

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
            conn.execute(self._SET_SQL, (key, data))

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
                conn.execute(self._ADD_SQL, (key, data))
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
            for row in conn.execute(self._DUMP_SQL,):
                res.append(row)
        return res

    def __del__(self):
        """
        Cleans up the object by destroying the sqlite connection.

        Returns:

        """
        if self.connection:
            self.connection.close()

    def purge(self) -> bool:
        """
        Remove the cache directory and all cache databases.

        Returns:
            bool:
        """
        if not os.path.isdir(self.cache_directory):
            return False

        try:
            shutil.rmtree(self.cache_directory)
        except OSError as e:
            logging.exception(e)
            return False
        else:
            return True

    def cleanup(self) -> bool:
        """
        Remove the cache database.

        Returns:
            bool:
        """
        if os.path.exists(self.cache_db):
            try:
                os.remove(self.cache_db)
            except OSError as e:
                logging.exception(e)
                raise
            else:
                return True

        return False
