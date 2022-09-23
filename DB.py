import os
import logging
import pymssql
import pandas as pd
from utils import get_credentials
import datetime
import zipfile

from retrieve_vault_creds import retrieve_vault_creds


# ReadTheDocs on the ms-sql python module
# https://pymssql.readthedocs.io/en/stable/intro.html

# GH repo for the code ...
# https://github.com/pymssql/pymssql

# probably should leverage these for our unit testing
# https://github.com/pymssql/pymssql/blob/master/tests/test_config.py

class DB(object):
    """DB() - class handles connecting, reading and writing various database tables"""

    def __init__(self, config_tag=None, config_file=None):
        """__init__() - provides parameters necessary to connect to database"""
        logging.debug(f"{__name__}:__init__({config_tag}, {config_file})")
        self.config_tag = config_tag
        self.config_file = config_file

        if self.config_file is None:
            self.config_file = ".mssql_db.conf"

        # choose the database to use
        if self.config_tag is None:
            self.config_tag = "dev"

        self.protocol = 'tcp'
        self.host, self.port, self.dbname, self.uid, self.pw = get_credentials(self.config_tag, self.config_file)

        self.conn = None
        self.cursor = None

        # call the method to really do the connection ...
        self.connect()

    def connect(self):
        """connect - to database with parameters specified
        """
        get_from_vault = True
        try:
            if get_from_vault:
                db_tag = 'hni'
                host, uid, pw, dbname = retrieve_vault_creds(db_tag)
            else:
                host, uid, pw, dbname = self.host, self.uid, self.pw, self.dbname
            self.conn = pymssql.connect(host, uid, pw, dbname)
            log_conn = \
                "DATABASE={database};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={uid};PWD={pw}".format(
                    database=self.dbname,
                    hostname=self.host,
                    port="8675309",
                    protocol=self.protocol,
                    uid="some_luser",
                    pw="ain't_gonna_tell",
                )
            logging.info(log_conn)

            return self.conn
        except Exception as ex:
            ex_message = f"Exception: {ex} cannot connect to {self.dbname}"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def get_cursor(self):
        """get_cursor() - return the current cursor"""
        try:
            self.cursor = self.conn.cursor()
            logging.debug("Returning Cursor")
            return self.cursor
        except Exception as ex:
            ex_message = f"Exception: {ex} cannot get cursor"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    # This will be implemented in data_table
    def execute(self, sql):
        """execute(sql) - execute sql statement, return the results"""
        try:
            pd_data = pd.read_sql_query(sql, self.conn)
            # self.cursor.execute(sql)
            logging.debug("Executing SQL Query")
            return pd_data
        except Exception as ex:
            ex_message = f"Exception: {ex} cannot execute sql query"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def fetch_one(self):
        """fetch_one - fetch a single record at the cursor"""
        return self.cursor.fetchone()

    def fetch_all(self):
        """fetch_all() records that match specfied criteria"""
        return self.cursor.fetchall()

    def insert(self, sql):
        """insert database record"""
        try:
            self.cursor.execute(sql)
            logging.debug("Executing Insert SQL Query")
        except Exception as ex:
            ex_message = f"Exception: {ex} cannot Insert into the Table"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def update(self, sql):
        """update database record"""
        try:
            self.cursor.execute(sql)
            logging.debug("Executing Update SQL Query")
        except Exception as ex:
            ex_message = f"Exception: {ex} cannot Update Table"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def upsert(self, inssql, updsql):
        """upsert to database (update and insert)"""
        try:
            self.cursor.execute(inssql)
            logging.debug("Executing Insert in upsert mode")
        except Exception as ex:
            # this is a DB2 exception, i forget what causes this, we worked around thsi
            if ex.args[0] == '23505':
                try:
                    self.cursor.execute(updsql)
                    logging.debug("Executing update in upsert mode")
                except Exception as ex:
                    ex_message = f"Exception: {ex} cannot Update Table in upsert mode"
                    logging.exception(ex_message)
                    raise RuntimeError(ex_message) from ex
            else:
                ex_message = f"Exception: {ex} cannot Insert Table"
                logging.exception(ex_message)
                raise RuntimeError(ex_message) from ex

    def commit(self):
        """commit to the database"""
        try:
            self.cursor.commit()
            logging.debug("Committing the Records")
        except Exception as ex:
            ex_message = f"Exception: {ex} cannot Commit Records"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def close_conn(self):
        """flush and close db connection"""
        try:
            logging.debug("Close DB connection {}".format(self.host))
            self.conn.close()
            self.conn = None  # fail fast if this is reused!
        except Exception as ex:
            ex_message = f"Exception: {ex} closing DB connection"
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def read_csv(self, input_file):
        """wrapper around pandas read_csv
        1. make sure file is readable, throw exception if not
        """

        if not os.access(input_file, os.R_OK):
            ex_message = f"PermissionError: [Errno 13] Permission denied: '{input_file}'"
            logging.exception(ex_message)
            raise RuntimeError(ex_message)

        if zipfile.is_zipfile(input_file):
            with zipfile.ZipFile(input_file, mode="r") as archive:
                for filename in archive.namelist():
                    print(f"unzipped file name is '{filename}'")
            # just print the file name for time being ...
            print(f"skipping ..., not currently processing zip files ... ")
            return

        stat_result = os.stat(input_file)
        num_of_bytes = stat_result.st_size
        file_mask = oct(os.stat(input_file).st_mode)[-3:]

        logging.debug(f"Input File: {input_file} is {stat_result.st_size} bytes and file mask is {file_mask}")
        if num_of_bytes > 50000:
            chunk = 10000
        else:
            chunk = 1000
        num_records = 0
        chunks = 0
        start_time = datetime.datetime.now()
        # for df in pd.read_csv(input_file, sep=",", engine="python", encoding="utf-8", chunksize=chunk, escapechar="\\"):
        for df in pd.read_csv(input_file, sep=",", engine="python", encoding='cp1252', chunksize=chunk,
                              escapechar="\\"):
            chunks += 1
            num_records += len(df)
            print(df)
        end_time = datetime.datetime.now()
        logging.debug(
            f"Processed:  records={num_records:,} in chunks={chunks}, chunk_size={chunk}, elapsed time={end_time - start_time}")
