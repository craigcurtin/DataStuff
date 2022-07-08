import logging
from DB import DB


class ETL(DB):
    """
        ETL - Extract Translate Load class for manipulating database tables
    """
    def __init__(self, config_tag=None, config_file=None):
        """class constructor"""
        logging.debug(f"{__name__}:__init__({config_tag}, {config_file})")
        # call base class to do any initialization ...
        super().__init__(config_tag, config_file)

        self.data = None

    def extract(self, key=None):
        """extract data from storage specified by key"""
        if key is None:
            extract_data = "SELECT TOP (5) *  FROM [controlTower].[tblEmail]"
        else:       # go extract data from a table ...
            extract_data = "SELECT TOP (1000) *  FROM [controlTower].[tblEmail]"

        self.data = self.execute(extract_data)
        logging.debug(extract_data)

    def transform(self, key=None):
        """transform data per key"""
        if key is None:
            transform_data = f"Transform whatever default is, key={key}"
        else:       # go extract data from a table ...
            transform_data = f"Transform specific to key={key}"

        logging.info(transform_data)

    def load(self, key=None):
        """load data back into store specified by key"""
        if key is None:
            load_data = f"Load whatever default is, key={key}"
        else:       # persist data to specfic table  ...
            load_data = f"Load specific to key={key}"

        logging.info(load_data)

