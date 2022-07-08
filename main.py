import os
import logging
import sys
from utils import setup_logger
from DB import DB
from ETL import ETL
from QueryEngine import QueryEngine

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    exe_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    setup_logger(exe_name, '/tmp', logging.INFO)
    db = DB()

    qry = 'SELECT TOP (10) *  FROM [controlTower].[qryLoadRouteListStatus]'
    df = db.execute(qry)

    # now invoke the QueryEngine()
    qe = QueryEngine()
    results_returned = qe.run()
    logging.debug(results_returned)

    results = qe.run(['foo'])
    logging.debug(results_returned)

    l = logging.getLogger()
    l.setLevel(logging.DEBUG)

    etl = ETL()
    etl.extract("foo")
    etl.transform("foo")
    etl.load("foo")
    #etl = None

    etl2 = ETL("dev")
    etl2.extract("bar")
    etl2.transform("bar")
    etl2.load("bar")


    logging.info('Normal Termination')
