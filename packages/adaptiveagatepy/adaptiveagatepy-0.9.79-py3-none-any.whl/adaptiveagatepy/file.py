# Copyright 2020, Adaptive Biotechnologies
''' Contains higher-level APIs for working with Agate files. '''

from contextlib import closing
import time
import traceback
from typing import List, Mapping

from . import config 
from . import item_cache
from . import related_files
from . import file_cache
from .related_files import RelatedFile

import logging
logger = logging.getLogger(__name__)

def ensure_files_for_items(config: config.Config, item_ids: str or List[str], keys: str or List[str], version = related_files.INCLUDE_CURRENT) -> List[RelatedFile]:
    ''' For a set of items, ensures files are in the cache and return local paths

    :param config: the configuration object 
    :type config: Config
    :param item_ids: a single item ID or list of item ID
    :type item_ids: str or List[str]
    :param keys: the file key(s) to download
    :type keys: str or List[str]
    :param version: the file version to download (default = most current version)
    :type version: str
    :return: a list of RelatedFile instances with the item_id and remote path to the file.
    :rtype: List[RelatedFile]
    '''
    if config is None:
        raise ValueError("The config value must be provided.")

    if not config.cache_directory:
        raise ValueError("The cache_directory must be provided in config.")

    if (not item_ids):
        raise ValueError("item_ids must be provided.")

    if (not keys):
        raise ValueError("keys must be provided.")

    start_time = time.time()

    id_list = list()
    if isinstance(item_ids, str):
        id_list.append(item_ids)
    else:
        id_list.extend(item_ids)

    key_list = list()
    if isinstance(keys, str):
        key_list.append(keys)
    else:
        key_list.extend(keys)

    server_files = []
    with item_cache.get_connection(config) as connection:
        with closing(connection.cursor()) as cursor:
            if version == related_files.INCLUDE_CURRENT:
                query = "select rf.item_id, rf.file_key, rf.file_version, rf.path, rf.upload_date, rf.md5_hash, rf.content_type " + \
                    "from related_files rf " + \
                    "inner join ( " + \
                    "select item_id, item_type, file_key, max(file_version) as file_version from related_files group by item_id, item_type, file_key " + \
                    ") rf_version on rf_version.item_id = rf.item_id and rf_version.item_type = rf.item_type and rf_version.file_key = rf.file_key and rf_version.file_version = rf.file_version " + \
                    "where rf.item_id in (" + ",".join(["?"] * len(id_list)) + \
                    ") and rf.file_key in (" + ",".join(["?"] * len(key_list)) + ")"
            else:
                query = "select rf.item_id, rf.file_key, rf.file_version, rf.path, rf.upload_date, rf.md5_hash, rf.content_type from related_files rf where rf.item_id in (" + \
                    ",".join(["?"] * len(id_list)) + \
                    ") and rf.file_key in (" + ",".join(["?"] * len(key_list)) + ")"

            cursor.execute(query, (*id_list, *key_list))
            server_files = [RelatedFile(item_id = r["item_id"], Key = r["file_key"], Version = r["file_version"], Path = r["path"], ContentType = r["content_type"], UploadDate = r["upload_date"], MD5Hash = r["md5_hash"])
                      for r in cursor.fetchall()]

    cached_related_files = file_cache.get_files(config, server_files)

    logger.info(f"Done ensuring files for {id_list} in %s seconds," % (time.time() - start_time))
    return cached_related_files

def __get_files_for_column(config: config.Config, table_filter: str or List[str], column: str, column_values: str or List[str], keys: str or List[str], version = related_files.INCLUDE_CURRENT) -> Mapping[str, RelatedFile]:

    column_value_list = list()
    if isinstance(column_values, str):
        column_value_list.append(column_values)
    else:
        column_value_list.extend(column_values)

    key_list = list()
    if isinstance(keys, str):
        key_list.append(keys)
    else:
        key_list.extend(keys)

    table_list = list()
    if isinstance(table_filter, str):
        table_list.append(table_filter)
    else:
        table_list.extend(table_filter)

    start_time = time.time()

    tables = [value for value in table_list if value in item_cache.table_names(config)]
    server_files = {}
    id_to_name = {}
    with item_cache.get_connection(config) as connection:
        with closing(connection.cursor()) as cursor:
            if version == related_files.INCLUDE_CURRENT:
                query_fmt = "select distinct table_alias.{column} as {column}, rf.item_id as item_id, rf.file_key as file_key, rf.file_version as file_version, rf.path as path, rf.upload_date as upload_date, rf.md5_hash as md5_hash, rf.content_type as content_type " + \
                    "from all_related_files rf " + \
                    "inner join ( " + \
                    "select item_id, item_type, file_key, max(file_version) as file_version from all_related_files group by item_id, item_type, file_key " + \
                    ") rf_version on rf_version.item_id = rf.item_id and rf_version.item_type = rf.item_type and rf_version.file_key = rf.file_key and rf_version.file_version = rf.file_version " + \
                    "inner join {table_name} table_alias on table_alias.item_id = rf.item_id " + \
                    "where table_alias.{column} in (" + ",".join(["?"] * len(column_value_list)) + \
                    ") and rf.file_key in (" + ",".join(["?"] * len(key_list)) + ") "
                query_parameters = (*column_value_list, *key_list)
            else:
                query_fmt = "select distinct table_alias.{column} as {column}, rf.item_id as item_id, rf.file_key as file_key, rf.file_version as file_verison, rf.path as path, rf.upload_date as upload_date, rf.md5_hash as md5_hash, rf.content_type  as content_type " + \
                    "from all_related_files rf " + \
                    "inner join {table_name} table_alias on table_alias.item_id = rf.item_id " + \
                    "where table_alias.{column} in (" + ",".join(["?"] * len(column_value_list)) + \
                    ") and rf.file_key in (" + ",".join(["?"] * len(key_list)) + ") and rf.file_version = ? "
                query_parameters = (*column_value_list, *key_list, version)

            # expand out the query and parameters for each item table
            query = " union ".join([query_fmt.format(table_name=t, column=column) for t in tables])
            query_parameters = query_parameters * len(tables)

            cursor.execute(query, query_parameters)
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            print(*column_names, sep=', ')
            server_files = [RelatedFile(item_id = r["item_id"], Key = r["file_key"], Version = r["file_version"], Path = r["path"], ContentType = r["content_type"], UploadDate = r["upload_date"], MD5Hash = r["md5_hash"])
                      for r in rows]
            id_to_name = {r["item_id"]: r[column] for r in rows}

    cached_related_files = file_cache.get_files(config, server_files)

    results = {id_to_name[rf.item_id]: rf for rf in cached_related_files}

    logger.info("Finished getting files by column in %s seconds." % (time.time() - start_time))
    return results
