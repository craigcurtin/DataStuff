import logging
import pymssql
import pandas as pd
from utils import get_credentials

# https://pymssql.readthedocs.io/en/stable/intro.html


class DB(object):
    """DB() - class handles connecting, reading and writing various database tables"""
    def __init__(self, config_tag=None, config_file=None):
        """__init__() - provides parameters necessary to connect to database"""
        logging.debug(f"{__name__}:__init__({config_tag}, {config_file})")
        if config_file is None:
            self.config_file = '.mssql_db.conf'

        # choose the database to use
        if config_tag is None:
            self.config_tag = 'dev'

        self.protocol = 'tcp'
        self.host, self.port, self.dbname, self.uid, self.pw = get_credentials(self.config_tag, self.config_file)

        self.conn = None
        self.cursor = None

        # call the method to really do the connection ...
        self.connect()


keyring
"""connect - to database with parameters specfied
        :return:
        """
        try:
            self.conn = pymssql.connect(self.host, self.uid, self.pw, self.dbname)
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
            logging.exception("Exception: {} cannot connect to {}".format(ex, self.dbname))
            raise RuntimeError("Exception: {} cannot connect to {}".format(ex, self.dbname)) from ex

    def get_cursor(self):
        """get_cursor() - return the current cursor"""
        try:
            self.cursor = self.conn.cursor()
            logging.debug("Returning Cursor")
            return self.cursor
        except Exception as ex:
            ex_message = "Exception: {} cannot get cursor".format(ex)
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
            ex_message = "Exception: {} cannot execute sql query".format(ex)
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
            ex_message = "Exception: {} cannot Insert into the Table".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def update(self, sql):
        """update database record"""
        try:
            self.cursor.execute(sql)
            logging.debug("Executing Update SQL Query")
        except Exception as ex:
            ex_message = "Exception: {} cannot Update Table".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def upsert(self, inssql, updsql):
        """upsert to database (update and insert)"""
        try:
            self.cursor.execute(inssql)
            logging.debug("Executing Insert in upsert mode")
        except Exception as ex:
            if ex.args[0] == '23505':
                try:
                    self.cursor.execute(updsql)
                    logging.debug("Executing update in upsert mode")
                except Exception as ex:
                    ex_message = "Exception: {} cannot Update Table in upser mode".format(ex)
                    logging.exception(ex_message)
                    raise RuntimeError(ex_message) from ex
            else:
                ex_message = "Exception: {} cannot Insert Table ".format(ex)
                logging.exception(ex_message)
                raise RuntimeError(ex_message) from ex

    def commit(self):
        """commit to the database"""
        try:
            self.cursor.commit()
            logging.debug("Committing the Records")
        except Exception as ex:
            ex_message = "Exception: {} cannot Commit Records".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex

    def close_conn(self):
        """flush and close db connection"""
        try:
            logging.debug("Close DB connection {}".format(self.host))
            self.conn.close()
        except Exception as ex:
            ex_message = "Exception: {} closing DB connection".format(ex)
            logging.exception(ex_message)
            raise RuntimeError(ex_message) from ex
