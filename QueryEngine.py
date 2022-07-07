import logging
from DB import DB
from qry_templates import simple_sql_queries, jinja_sql_queries
from jinja2 import Template

default_query_attributes = {
    'asset_classes': ['fx', 'equities', 'rates'],
    'cities': ['London', 'New York', 'Tokyo'],
    'duration': ['hour', 'day', 'week', 'month'],
    'baseball': ['cubs', 'mets', 'braves', 'white sox'],
    'football': ['bears', 'giants', 'bucs', 'cardinals', 'dolphins']
}


class QueryEngine(DB):
    """
        class QueryEngine()
        handles SQL/DB queries for both simple and jinja templated queries
        NOTES: kind of wondering if this should be derived from DB class for
        doing mash-up of DB access and templates etc.

        I could see DB Engine using Jinja Template and hitting DB in one call
    """
    def __init__(self, config_tag=None, config_file=None):
        logging.debug(f"{__name__}:__init__({config_tag}, {config_file})")
        # call base class to do any initialization ...
        super().__init__(config_tag, config_file)
        """constructor"""
        self.query_attributes_data = None
        self.templates = None
        self.query_attributes()

    def load_templates(self, fname):
        """load_templates from a file"""
        self.templates = fname

    def query_attributes(self, qa=None):
        """pass in query attributes for Jinja templates, if None, default dict will be used"""
        if qa is None:
            self.query_attributes_data = default_query_attributes
        else:
            self.query_attributes_data = qa

    def run(self, list_of_keys=None):
        """run - apply keys to templates, return result(s)"""
        results = []
        if list_of_keys is None:
            list_of_keys = ['foo', 'bar']

        for key in list_of_keys:
            qry = Template(jinja_sql_queries[key]).render(self.query_attributes_data)
            results.append(qry)

        logging.info(results)
        return results
        # df = db.execute(qry)
