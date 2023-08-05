''' Contains the APIs to help cache Agate items in a local SQLite database. '''
from contextlib import closing
from datetime import datetime
import logging
import os
import pyodbc
import sqlite3
import time
from time import mktime
import traceback
from typing import List, Mapping

from .config import Config
from . import db

logger = logging.getLogger(__name__)

def exists(config:Config) -> bool :
    if config is None:
        raise ValueError("The config value must be provided.")

    cache_path = get_cache_path(config)
    exists = os.path.exists(cache_path)
    if exists:
        with get_connection(config) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("select count(*) from sqlite_master where type='table'")
                table_count = cursor.fetchone()[0]
                exists = table_count > 0

    return exists

def clear(config:Config):
    if config is None:
        raise ValueError("The config value must be provided.")

    db_path = get_cache_path(config)
    
    if os.path.exists(db_path):
        os.remove(db_path)

def sync(config: Config, tables: List[str] = None):
    ''' Updates the Agate item cache database with the latest data from the server.
    
    :param config: the configuration object containing the cache_directory which specifies the location of the item cache.
    :type config: Config
    '''

    if config is None:
        raise ValueError("The config value must be provided.")

    sync_start = time.time()
    try:
        with get_connection(config) as local_connection:
            max_upload_date_tables = __get_max_upload_date_tables(local_connection, tables)
            agate_tables = __get_agate_tables(config)

            if (tables is not None):
                agate_tables = (t for t in agate_tables if t in tables)

            all_tables_upload_date = {}
            all_tables_upload_date.update(max_upload_date_tables)
            for agate_table in agate_tables:
                if (agate_table not in all_tables_upload_date):
                    all_tables_upload_date[agate_table] = time.gmtime(0)

            __sync_tables(config, local_connection, all_tables_upload_date)

    except Exception as e:
        logger.error('Unable to sync data from server. ' + traceback.format_exc())
        raise

    finally:
        logger.info("Sync completed in %s seconds." % (time.time() - sync_start) )

def get_connection(config: Config, auto_commit: bool = True) -> sqlite3.Connection :
    ''' Gets a connection to the local Agate item cache database

    :param config: the configuration object containing the cache_directory which specifies the location of the item cache.
    :type config: Config
    '''
    if config is None:
        raise ValueError("The config value must be provided.")

    connection = None
    try:
        if auto_commit:
            connection = sqlite3.connect(get_cache_path(config), isolation_level=None)
        else:
            connection = sqlite3.connect(get_cache_path(config))
    except Exception as e:
        logger.error("Unable to obtain a connection to the local item cache database. " + traceback.format_exc())
        raise

    # Makes it easy to access columns like a dictionary
    connection.row_factory = sqlite3.Row
    return connection

def get_cache_path(config:Config) -> str :
    if config is None:
        raise ValueError("The config value must be provided.")
    cache_directory_path = os.path.abspath(os.path.expanduser(config.cache_directory))
    if not os.path.exists(cache_directory_path):
        os.makedirs(cache_directory_path)

    path = os.path.join(cache_directory_path, 'items.db')
    return path

def table_names(config:Config) -> List[str] :
    table_names = []

    start_time = time.time()

    try:
        with get_connection(config) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("select name from sqlite_master where type='table'")
                table_rows = cursor.fetchall()

                for table_row in table_rows:
                    table_names.append(table_row[0])
    except:
        logger.error("Unable to retrieve the tables from the local item cache database. " + traceback.format_exc())
        raise

    logger.info("Retrieved local item cache tables in %s seconds" % (time.time() - start_time))
    return table_names

def __get_max_upload_date_tables(connection: sqlite3.Connection, tables: List[str] = None) -> Mapping[str, datetime]:
    '''Gets the maximum value of upload_date column in each table present'''
    start_time = time.time()

    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute("select name from sqlite_master where type='table'")
            table_rows = cursor.fetchall()

            table_names = []
            for table_row in table_rows:
                table_names.append(table_row[0])

            if (tables is not None):
                table_names = (t for t in table_names if t in tables)

            result = {}
            for table_name in table_names:
                with closing(connection.cursor()) as upload_date_cursor:
                    query = "select max(upload_date) from {0}".format(table_name)
                    upload_date_cursor.execute(query)
                    result[table_name] = upload_date_cursor.fetchone()[0]

            return result
    except:
        logger.error("Failed to retrieve the max upload_date from tables in the local item cache database. " + traceback.format_exc())
        raise
    finally:
        logger.info("Retrieved the max upload_date for the local tables in %s seconds." % (time.time() - start_time))

def __get_agate_tables(config: Config) -> List[str]:
    start_time = time.time()

    try:
        cursor = db.query(config, "select name from sys.views")
        names = [column[0] for column in cursor.fetchall()]
        return names
    except:
        logger.error("Failed to retrieve the list of tables from server. " + traceback.format_exc())
        raise
    finally:
        logger.info("Retrieved a list of server tables in %s seconds." % (time.time() - start_time))

def __sync_tables(config:Config, local_connection: sqlite3.Connection, tables_with_max_upload: Mapping[str, datetime]):
    agate_connection = db.get_connection(config)

    with agate_connection:
        filter_tables = [ 'item_tags', 'public_item_tags', 'public_anonymized_item_tags', 'anonymized_item_tags', 'item_related_files_with_json', 'database_firewall_rules']
        sync_tables = [table for table in tables_with_max_upload.items() if table[0] not in filter_tables]

        for table_and_upload_date in sync_tables:
            __sync_table(local_connection, agate_connection, table_and_upload_date)

def __sync_table(local_connection: sqlite3.Connection, agate_connection: pyodbc.Connection, table_name_upload_date:(str, datetime), max_sync_batch_size = 1000):
    start_time = time.time()
    table_name = table_name_upload_date[0]

    try:
        max_upload_date = __to_datetime(table_name_upload_date)

        with closing(agate_connection.cursor()) as agate_cursor:
            if (max_upload_date is None):
                query = "select * from {0}".format(table_name)
                agate_cursor.execute(query)
            else:
                query = "select * from {0} where upload_date > ?".format(table_name)
                agate_cursor.execute(query, (max_upload_date))

            if not __local_table_exists(local_connection, table_name):
                __create_local_table(table_name, local_connection, agate_cursor)

            column_names = [column[0] for column in agate_cursor.description if column[0] not in __filtered_columns]
            non_null_columns = [column[0] for column in agate_cursor.description if not column[6] and column[0] not in __filtered_columns]
            null_columns = [column[0] for column in agate_cursor.description if column[6] and column[0] not in __filtered_columns]
            columns_statement = ",".join(column_names)
            non_null_columns_statement = ",".join(non_null_columns)
            null_columns_statement = ", ".join(["{0}=excluded.{0}".format(column) for column in null_columns])

            # Need to restrict the number of parameters
            SQLITE_MAX_VARIABLE_NUMBER = 999 # defined by SQLITE documentation https://www.sqlite.org/limits.html
            batch_size = min([max_sync_batch_size, SQLITE_MAX_VARIABLE_NUMBER // len(column_names)])

            row = agate_cursor.fetchone()
            if row:
                with closing(local_connection.cursor()) as local_cursor:
                    while row:
                        batch_count = 0
                        row_values = []
                        values_statement = ""
                        while row and batch_count < batch_size:
                            row_values = row_values + [row.__getattribute__(column) for column in column_names]
                            if values_statement:
                                values_statement += ","

                            question_params = ",".join(["?"] * len(column_names))
                            values_statement += f"({question_params})"
                            row = agate_cursor.fetchone()
                            batch_count += 1

                        # Match the values retrieved from the data to those in the upsert statement
                        if (values_statement):
                            # Upsert isn't available in sqlite3 until 3.24 which doesn't ship with Python until 3.7. So instead
                            # of using upsert here I'm using 'insert or replace into' which still gets the semantics we need.
                            upsert_statement = f"insert or replace into {table_name} ({columns_statement}) Values {values_statement};" 
                            local_cursor.execute(upsert_statement, row_values)
            
                    local_connection.commit()
    except:
        logger.error(f"Failed to sync table {table_name} " + traceback.format_exc())
        raise
    finally:
        logger.info(f"Syncing table {table_name} completed in %s seconds." % (time.time() - start_time))

def __local_table_exists(local_connection: sqlite3.Connection, table_name: str) -> bool :
    with closing(local_connection.cursor()) as cursor:
        cursor.execute("select count(*) from sqlite_master where type='table' and name = ?", (table_name,))
        table_count = cursor.fetchone()[0]
        return table_count > 0

def __to_datetime(table_name_upload_date:(str, datetime)) -> datetime :
    some_date = table_name_upload_date[1]
    if some_date is None:
        return None
    if isinstance(some_date, datetime):
        return some_date
    elif isinstance(some_date, time.struct_time):
        return datetime.fromtimestamp(mktime(some_date))
    elif isinstance(some_date, str):
        try:
            return datetime.strptime(some_date, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return datetime.strptime(some_date, "%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError(str(some_date) + " of type " + str(type(some_date)) + " is not of an expected type for table " + table_name_upload_date[1] + ".")

__filtered_columns = [ 'related_files', 'current_rearrangement_tsv_file', 'current_extended_rearrangement_tsv_file', 'current_rearrangement_parquet_file', 'current_extended_rearrangement_parquet_file']

def __create_local_table(table_name: str, local_connection: sqlite3.Connection, agate_cursor:pyodbc.Cursor):
    start_time = time.time()

    try:
        pk_columns = [column[0] for column in agate_cursor.description if not column[6]]
        column_defs = ["{0} {1} {2}".format(column[0], __sqlite_type_from_sql_type(column[1], column[3]), "NULL" if column[6] else "NOT NULL" ) 
                       for column in agate_cursor.description
                       if column[0] not in __filtered_columns]

        create_table_statement = "create table if not exists {0} (\n".format(table_name) + ",\n".join(column_defs) + "\n, PRIMARY KEY(" + ",".join(pk_columns) + "));"
        logger.debug(f"Creating local table {table_name} as\n\n{create_table_statement}")

        with closing(local_connection.cursor()) as sqlite_cursor:
            sqlite_cursor.execute(create_table_statement)
    except:
        logger.error(f"Failed to create local table {table_name} " + traceback.format_exc())
        raise
    finally:
        logger.info(f"Creating local table {table_name} completed in %s seconds." % (time.time() - start_time))

def __string_type(precision):
    if precision == 0:
        return "text"
    else:
        return "varchar({0})".format(precision)

def __int_type(precision):
    return "int"

def __datetime_type(precision):
    return "datetime"

def __float_type(precision):
    return "float"

def __date_type(precision):
    return "date"

def __sqlite_type_from_sql_type(type_instance, precision) -> str:
    type_map = { 
        'str': __string_type,
        'int': __int_type,
        'datetime': __datetime_type,
        'float': __float_type,
        'date': __date_type
        }

    return type_map[type_instance.__name__](precision)