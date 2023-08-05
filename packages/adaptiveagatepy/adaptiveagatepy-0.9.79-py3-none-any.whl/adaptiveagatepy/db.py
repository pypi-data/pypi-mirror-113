# Copyright 2020, Adaptive Biotechnologies
''' Contains APIs for interacting with the Agate database. '''
import pyodbc
import struct
import time
import traceback

from . import azure_token_provider
from .config import Config

import logging
logger = logging.getLogger(__name__)

def query(config: Config, query: str) -> pyodbc.Cursor:
    ''' Queries the Agate database using the specified configuration string and query.
    
    :param config: the configuration object from which Agate user credentials and database connection strings are provided.
    :type config: Config
    :param query: the query to run against the Agate database.
    :type query: str

    :return: A cursor representing the results of the query. See PYODBC documentation for more information on how to use the cursor.
    :rtype: pyodbc.Cursor
    '''

    start_time = time.time()
    connection = get_connection(config)

    cursor = connection.cursor()
    cursor.execute(query)
    logger.debug(f"Finished executing query in %s seconds:\n{query}" % (time.time() - start_time))

    return cursor

def get_connection_string(config: Config) -> str:
    ''' Gets a PYODBC compliant connection string to the Agate database.

    :param config: the configuration object from which to get the db host, port, and name.
    :type config: Config

    :return: a PYODBC compliant connection string for querying the Agate database.
    :rtype: str
    '''
    if config is None:
        raise ValueError("The config value must be provided.")

    if not config.db_host:
        raise ValueError("The db_host must be provided.")

    if not config.db_port:
        raise ValueError("The db_port must be provided.")

    if not config.db_name:
        raise ValueError("The db_name must be provided.")

    connection_string_template =  "driver={};server={};port={};database={};"
    connection_string = connection_string_template.format("ODBC Driver 17 for SQL Server", config.db_host, config.db_port, config.db_name)
    return connection_string

def get_connection(config: Config) -> pyodbc.Connection:
    ''' Gets a PYODBC connection to the Agate database using the specified configuration.

    :param config: the configuration object form which to get the user credentials, database host, port, and name.
    :type config: Config

    :return: A PYODBC connection to the Agate database. Please see the PYODBC documentation on how this connection can be used.
    :rtype: pyodbc.Connection
    '''
    if config is None:
        raise ValueError("The config value must be provided.")

    connection_string = get_connection_string(config)

    if not config.agate_username:
        raise ValueError("The agate_username must be provided in config.")

    # blank = device flow
    #if not config.agate_password:
    #    raise ValueError("The agate_password must be provided in config.")

    if not config.app_client_id:
        raise ValueError("The app_client_id must be provided in config.")

    if not config.tenant_id:
        raise ValueError("The tenant_id must be provided in config.")

    start_time = time.time()

    try:
        access_token = azure_token_provider.get_access_token_with_config(azure_token_provider.SQL_RESOURCE, config)

        # Need to convert the token to the format expected by the ODBC driver. 
        # See https://github.com/AzureAD/azure-activedirectory-library-for-python/wiki/Connect-to-Azure-SQL-Database
        # and https://www.linkedin.com/pulse/using-azure-ad-service-principals-connect-sql-from-python-andrade
        SQL_COPT_SS_ACCESS_TOKEN = 1256 
        #get bytes from token obtained
        tokenb = bytes(access_token, "UTF-8")
        exptoken = b'';
        for i in tokenb:
            exptoken += bytes({i});
            exptoken += bytes(1);
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;

        connection = pyodbc.connect(connection_string, attrs_before = { SQL_COPT_SS_ACCESS_TOKEN:tokenstruct })
        return connection

    except Exception as e:
        logger.error('Unable to make connection to database. ' + traceback.format_exc())
        raise

    finally:
        logger.debug("Made connection to database in %s seconds." % (time.time() - start_time))





