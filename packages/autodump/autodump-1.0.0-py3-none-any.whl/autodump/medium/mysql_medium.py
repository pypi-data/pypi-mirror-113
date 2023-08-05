# -*- coding: utf-8 -*-

from autodump.main import *
from mysql import connector
import mysql.connector.pooling
import logging

from .common import *


class MysqlMedium(Medium):
    POOL_SIZE = 10
    REQUIRED_PARAM = ["host", "user", "port", "password", "database"]

    def __init__(self, space, param):
        super(MysqlMedium, self).__init__(param)
        self._table = space
        self._source = [None]
        self._reconnect()
        if not self._table_exists(self._table):
            self._new_table(self._table)
        self._cache = {}
        self._persistence = {}

    # TODO: Add and flush asynchronously, a good choice is using message queue
    def cache(self, k, v):
        self._cache[k] = v

    def flush(self):
        cache = {**self._persistence, **self._cache}
        for k in cache:
            if not self._column_exists(k):
                self._new_column(k)
        self._insert_cache(cache)

    def persist(self, k, v):
        self._persistence[k] = v

    def _check_param(self):
        if sorted(MysqlMedium.REQUIRED_PARAM) != sorted(list(self._param.keys())):
            raise Exception(
                "Invalid param, required param is: %s, your input is: %s" % (
                    MysqlMedium.REQUIRED_PARAM, self._param.keys()))

    def _reconnect(self):
        source = connector.pooling.MySQLConnectionPool(
            pool_name="pool.%s.%s" % (self._param["host"], self._param["database"]),
            pool_size=MysqlMedium.POOL_SIZE,
            **self._param)
        self._source[0] = source

    def activate(self):
        self._reconnect()

    # TODO: 1. Add INT and DOUBLE type, save priority: INT, DOUBLE, VARCHAR(255)
    #       2. Persistent kv: insert every time
    def _insert_cache(self, cache):
        SQL = ("INSERT INTO {0} ({1}) VALUES (" + (', '.join((["%s"]*len(cache.keys())))) + ")").format(self._table, (", ".join([str(key) for key in cache.keys()])))
        value = list(cache.values())
        self._execute(SQL, value)
        self._cache.clear()

    def _column_exists(self, k):
        SQL = "SHOW COLUMNS FROM {0} LIKE %s".format(self._table)
        value = [k]
        rowcount = self._execute(SQL, value)
        return rowcount != 0

    def _new_column(self, k):
        # Can not use placeholder for table names
        SQL = "ALTER TABLE {0} ADD {1} VARCHAR(1023)".format(self._table, k)
        value = []
        return self._execute(SQL, value)

    def _table_exists(self, table):
        SQL = "SHOW TABLES LIKE %s"
        value = [table]
        rowcount = self._execute(SQL, value)
        return rowcount != 0

    def _new_table(self, table):
        SQL = "CREATE TABLE {0} (id INT NOT NULL AUTO_INCREMENT, time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id))".format(table)
        value = []
        return self._execute(SQL, value)

    # TODO: Handle Exception
    def _execute(self, SQL, value):
        connection = self._source[0].get_connection()
        cursor = connection.cursor()
        # TODO: See if there is better way
        value = [str(_value).replace('\'', '\'\'') for _value in value]
        cursor.execute(SQL, value)
        cursor.fetchall()
        rowcount = cursor.rowcount
        connection.commit()
        connection.close()
        return rowcount
