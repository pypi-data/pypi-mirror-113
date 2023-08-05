# Copyright 2020, Adaptive Biotechnologies
''' Contains APIs to help manipulate the related_files Agate database JSON format and download files. '''

from azure.core.credentials import AccessToken
from azure.storage.blob import BlobClient
from datetime import datetime
from functools import partial
import json
import multiprocessing
from multiprocessing.pool import Pool
import os
import requests
import time
import traceback
from typing import List, Iterator, Tuple
from urllib.parse import urlparse

from . import db
from . import azure_token_provider
from .config import Config

import logging
logger = logging.getLogger(__name__)

INCLUDE_CURRENT = "CURRENT"

class RelatedFile:
    ''' A class representation of the JSON related_files format found in the Agate database. '''
    def __init__(self, Key: str, Version: str, Path: str, UploadDate: str, MD5Hash: str = None, ContentType: str = None, item_id: str = None):
        ''' Constructs a RelatedFile instance.

        :param Key: the file type key
        :type Key: str
        :param Version: the file version
        :type Version: str
        :param Path: can be either the Agate file URL or a pointer to a locally cached file.
        :type Path: str
        :param ContentType: the content type of the file.
        :type ContentType: str
        :param UploadDate: the uninterpreted date string stamped on the file at creation time.
        :type UploadDate: str
        :param MD5Hash: the MD5 hash of the file contents.
        :type MD5Hash: str
        :param item_id: the unique identifier of the Agate item that this file is related to. May be None if not known.
        :type item_id: str
        '''
        self.file_key = Key
        self.file_version = Version
        self.path = Path
        self.upload_date = UploadDate
        self.md5_hash = MD5Hash
        self.content_type = ContentType
        self.item_id = item_id

    def __str__(self):
        return json.dumps(self)

def from_json(related_files_json: Tuple[str, str] or List[Tuple[str, str]], filter_keys: List[str] = list(), filter_versions: List[str] = list()) -> List[RelatedFile]:

    result = list()
    
    related_files_jsons = list()

    include_current = INCLUDE_CURRENT in filter_versions
    
    if isinstance(related_files_json, Tuple):
        related_files_jsons.append(related_files_json)
    else:
        related_files_jsons.extend(related_files_json)

    for item_id, related_files_json_str in related_files_jsons:
        related_files_json = json.loads(related_files_json_str)
        for key, related_files in related_files_json.items():
            if (not filter_keys or key in filter_keys):
                # special case for current version ... note assumption that "CURRENT" will
                # not ever match a real version string which seems safe
                included_current_version = None
                if include_current:
                    related_file_dict = related_files[0]
                    related_file = RelatedFile(Key=related_file_dict.get("Key"), Version=related_file_dict.get("Version"), Path=related_file_dict.get("Path"), UploadDate=related_file_dict.get("UploadDate"), MD5Hash=related_file_dict.get("MD5Hash"), ContentType=related_file_dict.get("ContentType"), item_id=item_id)
                    result.append(related_file)
                    included_current_version = related_file.file_version

                # don't need to check key again because it's the same for all of these
                for related_file_dict in related_files:
                    if (not filter_versions or related_file_dict["Version"] in filter_versions):
                        related_file = RelatedFile(Key=related_file_dict.get("Key"), Version=related_file_dict.get("Version"), Path=related_file_dict.get("Path"), UploadDate=related_file_dict.get("UploadDate"), MD5Hash=related_file_dict.get("MD5Hash"), ContentType=related_file_dict.get("ContentType"), item_id=item_id)
                        if (related_file.file_version != included_current_version):
                            result.append(related_file)

    return result

def download_related_files(config: Config, related_files: RelatedFile or List[RelatedFile], destination: str = None, block_size = 1024) -> Iterator[RelatedFile]:
    if config is None:
        raise ValueError("The config value must be provided.")

    if not config.agate_username:
        raise ValueError("The agate_username must be provided in config.")

    if not config.app_client_id:
        raise ValueError("The app_client_id must be provided in config.")

    if not config.tenant_id:
        raise ValueError("The tenant_id must be provided in config.")

    start_time = time.time()

    try:
        file_destination = destination
        if not destination:
            if not config.cache_directory:
                raise ValueError("The cache_directory must be provided in config.")
            file_destination = config.cache_directory

        related_files_real = list()

        if isinstance(related_files, RelatedFile):
            related_files_real.append(related_files)
        else:
            related_files_real.extend(related_files)

        access_token = azure_token_provider.get_access_token_with_config(azure_token_provider.STORAGE_RESOURCE, config)

        results = list()

        for related_file in related_files_real:
            result_related_file = __download_related_file(related_file = related_file, access_token = access_token, config = config, destination = file_destination, block_size = block_size)
            results.append(result_related_file)

    finally:
        logger.info(f"Completed download of files in %s seconds." % (time.time() - start_time))

    return results

def __download_related_file(related_file, access_token, config, destination, block_size):
    local_path = __download_file(url = related_file.path, access_token = access_token, config = config, destination = destination, block_size = block_size)
    return RelatedFile(
        Key = related_file.file_key, 
        Version = related_file.file_version, 
        Path = local_path, 
        UploadDate = related_file.upload_date, 
        MD5Hash = related_file.md5_hash,
        ContentType = related_file.content_type, 
        item_id = related_file.item_id)
    
def download_files(config: Config, urls: List[str], destination: str = None, block_size: int = 1024) -> List[RelatedFile]:
    if config is None:
        raise ValueError("The config value must be provided.")

    if not config.agate_username:
        raise ValueError("The agate_username must be provided in config.")

    if not config.app_client_id:
        raise ValueError("The app_client_id must be provided in config.")

    if not config.tenant_id:
        raise ValueError("The tenant_id must be provided in config.")

    start_time = time.time()

    try:
        file_destination = destination
        if not destination:
            if not config.cache_directory:
                raise ValueError("The cache_directory must be provided in config.")
            file_destination = config.cache_directory

        access_token = azure_token_provider.get_access_token_with_config(azure_token_provider.STORAGE_RESOURCE, config)

        results = list()

        for url in urls:
            related_file = __download_file(url, access_token = access_token, config = config, destination = file_destination, block_size = block_size)
            results.append(related_file)

        return results
    finally:
        logger.info(f"Completed download of files {str(urls)} in % seconds." % (time.time() - start_time))

def download_file(config: Config, url: str, destination: str = None, block_size: int = 1024) -> str:
    if config is None:
        raise ValueError("The config value must be provided.")

    if not config.agate_username:
        raise ValueError("The agate_username must be provided in config.")

    if not config.app_client_id:
        raise ValueError("The app_client_id must be provided in config.")

    if not config.tenant_id:
        raise ValueError("The tenant_id must be provided in config.")

    start_time = time.time()

    try:
        file_destination = destination
        if not destination:
            if not config.cache_directory:
                raise ValueError("The cache_directory must be provided in config.")
            file_destination = os.path.abspath(os.path.expanduser(config.cache_directory))

        access_token = azure_token_provider.get_access_token_with_config(azure_token_provider.STORAGE_RESOURCE, config)
        return __download_file(url, access_token, config, file_destination, block_size)
    finally:
        logger.info(f"Completed download_file for {url} in % seconds." % (time.time() - start_time))

class AccessTokenCredential(object):
    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_token(self, *scopes, **kwargs):
        return AccessToken(self.access_token, expires_on=0)

def __download_file(url: str, access_token: str, config: Config, destination: str = None, block_size: int = 1024) -> str:

    abs_cache_directory = os.path.abspath(destination)
    os.makedirs(abs_cache_directory, exist_ok=True)

    headers = { 'Authorization': "Bearer {}".format(access_token), 'x-ms-version': '2017-11-09', 'x-ms-date': __format_utc_time() }

    local_path = os.path.join(abs_cache_directory, os.path.basename(url))

    parsed_url = urlparse(url)
    account_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    container_name = os.path.dirname(parsed_url.path)[1:]
    blob_name = parsed_url.path[len(container_name)+2:]

    blob_client = BlobClient(account_url, container_name, blob_name, credential=AccessTokenCredential(access_token))
    with open(local_path, "wb+") as local_file:
        blob_client.download_blob().readinto(local_file)

    return local_path

def __format_utc_time():
    return datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
