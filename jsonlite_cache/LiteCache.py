"""
Key-value storage with optional persistence for Python3 programs using SQLite3.

jsonlite_cache/LiteCache.py
"""

import os
import json
import shutil
import logging

from sqlite3 import Connection, IntegrityError


class LiteCache:
    """
    LiteCache
    """
    _create_sql = (
        'CREATE TABLE IF NOT EXISTS entries '
        '( key TEXT PRIMARY KEY, val BLOB )'
    )
    _create_index = 'CREATE INDEX IF NOT EXISTS keyname_index ON entries (key)'
    _get_sql = 'SELECT val FROM entries WHERE key = ?'
    _dump_sql = 'SELECT * from entries'
    _del_sql = 'DELETE FROM entries WHERE key = ?'
    _set_sql = 'REPLACE INTO entries (key, val) VALUES (?, ?)'
    _add_sql = 'INSERT INTO entries (key, val) VALUES (?, ?)'
    _clear_sql = 'DELETE FROM entries'

    connection = None
    cache_dir = None
    cache_db = None
    error_callback = None

    def __init__(self, app_name: str):
        """

        Args:
            app_name: str -
        """
        assert app_name, 'app_name cannot be blank'
        assert isinstance(app_name, str), 'app_name must be a string'

        # Set the app's cache directory path
        cache_base_dir = os.path.join(os.path.expanduser('~'), '.py-cache')

        # Check if the directory exists
        if not os.path.isdir(cache_base_dir):
            try:
                # Create the directory
                os.mkdir(cache_base_dir)

            except OSError as e:
                logging.exception(e)
                raise

        # Set the cache db file
        self.cache_dir = os.path.join(cache_base_dir, app_name)

        # Check if the directory exists
        if not os.path.isdir(self.cache_dir):
            try:
                # Create the directory
                os.mkdir(self.cache_dir)

            except OSError as e:
                logging.exception(e)
                raise

        # Set the cache db file path
        cache_file = os.path.join(self.cache_dir, '{}.db'.format(app_name))
        self.cache_db = cache_file

    def flush(self) -> bool:
        """
        Flush the database tables.

        Returns:
            bool:
        """
        with self._get_conn() as conn:
            try:
                conn.execute(self._clear_sql)
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
