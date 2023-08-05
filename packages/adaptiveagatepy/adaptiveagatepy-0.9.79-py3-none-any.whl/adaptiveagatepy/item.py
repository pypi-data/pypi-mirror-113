# Copyright 2020, Adaptive Biotechnologies
''' Provides high-level APIs for retrieving items from the Agate platform. 
The db, file_cache, and related_files modules all provide lower level access to the Agate platform, requiring you to put the pieces together. 
These APIs do the work for you. As long as your query returns the item_id and related_files columns, these APIs will help you join the database
data to the file data as appropriate. You can even use your dataframe of choice, as long as it's Pandas or Dask.
'''
from contextlib import closing
from functools import reduce
import dask
import dask.dataframe as dd
import pandas
import pyarrow
import pyarrow.parquet as pq
from sqlite3 import Cursor, Row
import time
import traceback
from typing import Dict, List, Tuple

from .config import Config
from . import db
from . import file
from . import file_cache
from . import item_cache
from . import related_files
from adaptiveagatepy.related_files import RelatedFile

import logging
logger = logging.getLogger(__name__)

class AgateItem:
    ''' Represents an item from the Agate database.
    When you run a query using the query API, you can convert the result to a list of AgateItems. Each
    column returned becomes a property of the AgateItem instance.
    '''
    def __init__(self, db_columns: List[str], db_row: Row):
        for column in db_columns:
            setattr(self, column, db_row[column])

def items_to_pandas(config: Config, query: str, *query_parameters) -> pandas.DataFrame:
    ''' Converts the Agate database result to a Pandas DataFrame. 
        
    :return: a Pandas DataFrame containing the query results.
    :rtype: pandas.DataFrame
    '''
    if config is None:
        raise ValueError("The config value must be provided.")

    if query is None:
        raise ValueError("The query must be provided.")

    if not item_cache.exists(config):
        raise AssertionError("The item_cache must be initialized by calling item_cache.sync() before calling this method.")

    start_time = time.time()
    try:
        with item_cache.get_connection(config) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, *query_parameters)
                df = pandas.DataFrame([tuple(row) for row in cursor.fetchall()])
                df.columns = [column[0] for column in cursor.description]

                return df
    finally:
        logger.info(f"Completed items_to_pandas for {query} in %s seconds." % (time.time() - start_time))

def items_and_files_to_pandas(config: Config, query: str, file_key: str or List[str], file_version = related_files.INCLUDE_CURRENT, *query_parameters) -> pandas.DataFrame:
    ''' Converts the Agate database result and related files to a Pandas DataFrame. 
    Note, it is not recommended to use Pandas for large datasets. Pandas loads all the data into memory
    and can easily overwhelm most computers. It is recommended to use Dask for large amounts of data.

    :param config: the configuration containing the database host, port, and name, as well as the Agate user credentials.
    :type config: Config
    :param query: the query to run against the Agate database. It must include item_id as a column in the select fields.
    :type query: str
    :param file_key: the related file type to join to the query columns. For sequence data it is recommended to use "REARRANGEMENT_PARQUET".
    :type file_key: str

    :return: A Pandas DataFrame containing the joining of the query results and the data in the related files for those results.
    :rtype: pandas.DataFrame
    '''
    if file_key is None:
        raise ValueError("The file_key parameter must be provided.")

    start_time = time.time()

    try:
        # turn the items into a dataframe
        item_df = items_to_pandas(config, query, *query_parameters)

        # grab the related files from the item cache by using the item_id from the query results
        files = file.ensure_files_for_items(config, item_df['item_id'].tolist(), file_key, file_version)

        # load the files into separate dataframes
        item_file_dfs = list()
        for local_file in files:
            try:
                # load the file into a dataframe based on the type of the file
                if "TSV" in file_key:
                    file_df = pandas.read_csv(local_file.path, sep='\t')
                elif "PARQUET" in file_key:
                    file_df = pq.read_table(local_file.path).to_pandas()
            except pandas.io.common.EmptyDataError:
                continue

            # Add the item_id to the file rows so that we can join with the item_df
            file_df['item_id'] = local_file.item_id
            item_file_df = pandas.merge(item_df, file_df, on="item_id")
            item_file_dfs.append(item_file_df)

        # finally concat all the data frames together
        return pandas.concat(item_file_dfs, axis=0, ignore_index=True)
    finally:
        logger.info(f"Completed items_and_files_to_pandas for {query} in %s seconds." % (time.time() - start_time))

def items_to_pandas_and_local_files(config: Config, query: str, file_key: str or List[str], file_version = related_files.INCLUDE_CURRENT, *query_parameters) -> Tuple[pandas.DataFrame, Dict[str, str]]:
    ''' Converts the Agate database result to a Pandas DataFrame and downloads the related files
    and returns them as a dictionary of item_id to local file path.

    :param config: the configuration containing the database host, port, and name, as well as the Agate user credentials.
    :type config: Config
    :param query: the query to run against the Agate database. It must include item_id as a column in the select fields.
    :type query: str
    :param file_key: the related file type to join to the query columns. For sequence data it is recommended to use "REARRANGEMENT_PARQUET".
    :type file_key: str
    :param file_version: the related file version to include in the file list.
    :type file_version: str

    :return: A Pandas DataFrame containing the query results and a dictionary containing a map of the item_id to the local file for the related files.
    :rtype: Tuple
    '''

    if file_key is None:
        raise ValueError("The file_key parameter must be specified.")

    start_time = time.time()

    try:
        # turn the items into a dataframe
        item_df = items_to_pandas(config, query, *query_parameters)

        # grab the related files from the item cache by using the item_id from the query results
        files = file.ensure_files_for_items(config, item_df['item_id'].tolist(), file_key, file_version)

        # Generate a map of item_id to file path
        local_files = {}
        for local_file in files:
            # Add the item_id to the file rows so that we can join with the item_df
            local_files[local_file.item_id] = local_file.path

        return (item_df, local_files)
    finally:
        logger.info(f"Completed items_to_pandas_and_local_files for {query} in %s seconds." % (time.time() - start_time))

def items_to_dask(config: Config, query: str, npartitions = None, chunksize = None, *query_parameters) -> dask.dataframe:
    ''' Converts the Agate database result to a Dask DataFrame. 
        
    :param config: the configuration containing the database host, port, and name, as well as the Agate user credentials.
    :type config: Config
    :param query: the query to run against the Agate database. It must include item_id as a column in the select fields.
    :type query: str

    :return: a Dask DataFrame containing the query results.
    :rtype: dask.DataFrame
    '''

    start_time = time.time()
    try:
        df = items_to_pandas(config, query, *query_parameters)
        return dd.from_pandas(df, npartitions=npartitions, chunksize=chunksize)
    finally:
        logger.info(f"Completed items_to_dask for {query} in %s seconds." % (time.time() - start_time))

def items_and_files_to_dask(config: Config, query: str, file_key: str or List[str], file_version = related_files.INCLUDE_CURRENT, npartitions = None, chunksize = None, *query_parameters) -> dask.dataframe:
    ''' Converts the Agate database result and related files to a Dask DataFrame. 

    :param config: the configuration containing the database host, port, and name, as well as the Agate user credentials.
    :type config: Config
    :param query: the query to run against the Agate database. It must include item_id as a column in the select fields.
    :type query: str
    :param file_key: the related file type to join to the query columns. For sequence data it is recommended to use "REARRANGEMENT_PARQUET".
    :type file_key: str or List[str]
    :param file_version: the related file version or "CURRENT" to include the latest version of each file.
    :type file_version: str or List[str]
    :param npartitions: the number of partitions to separate the Dask DataFrame into (default: None)
    :type npartitions: int
    :param chunksize: the size of the chunk for each partition (default: None)
    :type chunksize: int

    Either npartitions or chunksize must be specified. See the Dask DataFrame documentation for recommendations.

    :return: A Dask DataFrame containing the joining of the query results and the data in the related files for those results.
    :rtype: dask.DataFrame
    '''

    start_time = time.time()

    try:
        # turn the items into a dataframe
        item_df = items_to_pandas(config, query, *query_parameters)

        # grab the related files from the item cache by using the item_id from the query results
        files = file.ensure_files_for_items(config, item_df['item_id'].tolist(), file_key, file_version)

        # load the files into separate dataframes
        item_file_dfs = list()
        for local_file in files:
            try:
                # load the file into a dataframe based on the type of the file
                if "TSV" in file_key:
                    file_df = dd.read_csv(local_file.path, sep='\t')
                elif "PARQUET" in file_key:
                    file_df = dd.read_parquet(local_file.path)
            except pandas.io.common.EmptyDataError:
                continue

            # Add the item_id to the file rows so that we can join with the item_df
            file_df['item_id'] = local_file.item_id
            item_file_df = file_df.merge(item_df, how='inner', on="item_id")
            item_file_dfs.append(item_file_df)

        # finally concat all the data frames together
        return dd.concat(item_file_dfs)
    finally:
        logger.info(f"Completed items_and_files_to_dask for {query} in %s seconds" % (time.time() - start_time))

def items_to_list(config: Config, query: str, *query_parameters) -> List[AgateItem]:
    ''' Converts the Agate database result to a list of Agate items. 
        
    :param config: the configuration containing the database host, port, and name, as well as the Agate user credentials.
    :type config: Config
    :param query: the query to run against the Agate database. 
    :type query: str
        
    :return: a list of Agate items. Each row of the query result is a single item with attributes for each of the columns.
    :rtype: List[AgateItem]
    '''  
    if config is None:
        raise ValueError("The config value must be provided.")
    
    if query is None:
        raise ValueError("The query must be provided.")

    if not item_cache.exists(config):
        raise AssertionError("The item_cache must be initialized by calling item_cache.sync() before calling this method.")

    start_time = time.time()

    try:
        with item_cache.get_connection(config) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query, *query_parameters)
                columns = [column[0] for column in cursor.description]

                result = list()
                for row in cursor:
                    result.append(AgateItem(columns, row))

                return result
    finally:
        logger.info(f"Completed items_to_list for {query} in %s seconds." % (time.time() - start_time))




