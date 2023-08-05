# Copyright 2020, Adaptive Biotechnologies
''' Contains the APIs to help cache Agate data files in local storage and fetch them on demand. '''
import json
import os
import shutil
import time
import traceback
from typing import List, Tuple, Mapping

from .config import Config
from . import db
from . import related_files
from .related_files import RelatedFile

import logging
logger = logging.getLogger(__name__)

def clear_all(config: Config):
    ''' Clears all files from the file subdirectory of the cache_directory in the configuration object.
    
    :param config: the configuration object containing the cache_directory which specifies the location of the file cache.
    :type config: Config
    '''
    cache_directory = get_cache_directory(config)
    if os.path.exists(cache_directory):
        shutil.rmtree(cache_directory, ignore_errors=True)

    logger.info(f"File cache cleared: {cache_directory}")

def get_cache_directory(config: Config):
    return os.path.join(os.path.abspath(os.path.expanduser(config.cache_directory)), "files")

def get_files(config: Config, related_file_list: RelatedFile or List[RelatedFile]) -> List[RelatedFile]:
    ''' Gets the file(s) specified from the cache or downloads them if necessary. 

    :param config: the configuration object containing the cache_directory and the Agate user credentials required to download files.
    :type config: Config
    :param related_file_list: a list of the files to read from the cache or download if necessary. This parameter comes from the related_files column in the database and can be converted from JSON to a RelatedFile instance using the related_files module.
    :type related_file_list: RelatedFile or List[RelatedFile]

    :return: a list of the files with paths pointing to the local cache directory files rather than the server files.
    :rtype: List[RelatedFile]
    '''
    if config is None:
        raise ValueError("The config value must be provided.")

    if not config.cache_directory:
        raise ValueError("The cache_directory must be provided in config.")

    related_file_items = list()
    if isinstance(related_file_list, RelatedFile):
        related_file_items.append(related_file_list)
    else:
        related_file_items.extend(related_file_list)

    logger.debug(f"File cache query: {str(related_file_items)}")
    local_paths = list()
    needs_downloading = list()
    for related_file_item in related_file_items:
        if not __is_local_path(related_file_item.path):
            file_name = os.path.basename(related_file_item.path)
            file_path = os.path.abspath(os.path.join(get_cache_directory(config), file_name))
            if os.path.exists(file_path) and __timestamp_ok(file_path, related_file_item.upload_date):
                logger.debug(f"File cache hit: {file_path}")
                local_paths.append(RelatedFile(Key=related_file_item.file_key, Version=related_file_item.file_version, Path=file_path, UploadDate=related_file_item.upload_date, MD5Hash=related_file_item.md5_hash, ContentType=related_file_item.content_type, item_id=related_file_item.item_id))
            else:
                logger.debug(f"File cache miss: {file_path}")
                needs_downloading.append(related_file_item)
        else:
            local_path = related_file_item.path
            if not os.path.exists(local_path):
                raise FileNotFoundError("related_files specified a local path that does not exist. Either pass a URL to the related file in the cloud or a local path to a file that exists.")
            logger.debug(f"File cache hit: {local_path}")
            local_paths.append(RelatedFile(Key=related_file_item.key, Version=related_file_item.file_version, Path=local_path, UploadDate=related_file_item.upload_date, MD5Hash=related_file_item.md5_hash, ContentType=related_file_item.content_type, item_id=related_file_item.item_id))

    if len(needs_downloading) > 0:
        downloaded_file_paths = related_files.download_related_files(config, needs_downloading, get_cache_directory(config))
        __write_timestamps(downloaded_file_paths)
        local_paths.extend(downloaded_file_paths)

    return local_paths

def __is_local_path(path: str) -> bool :
    result = False
    try:
        schemeEndIndex = path.index("://") # Will throw a ValueError if it doesn't exist
        if path.startswith("file://"):
            result = True
    except ValueError as e:
        result = True

    return result

__TS_FILE_SUFFIX = "_created.txt"

def __write_timestamps(local_related_files):
    for local_related_file in local_related_files:
        timestamp_path = local_related_file.path + __TS_FILE_SUFFIX
        with open(timestamp_path, "w") as ts_file:
            ts_file.write(local_related_file.upload_date)

def __timestamp_ok(local_file_path, current_upload_date):
    timestamp_path = local_file_path + __TS_FILE_SUFFIX
    if not os.path.exists(timestamp_path): return False
    with open(timestamp_path, "r") as ts_file:
        existing_timestamp = ts_file.read()
        return existing_timestamp == current_upload_date

