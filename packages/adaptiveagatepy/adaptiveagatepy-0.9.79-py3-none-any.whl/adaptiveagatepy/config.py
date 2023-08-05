# Copyright 2020, Adaptive Biotechnologies
''' Contains the configuration class which is passed to most of the AdaptiveAgatePy APIs '''

import os
import copy
import sys
import json
import multiprocessing
import threading
import time
import traceback

import logging
logger = logging.getLogger(__name__)

class Config(object):
    '''
    Contains configuration information needed for most of the AdaptiveAgatePy APIs. Most of these values can
    be found with the documentation for the Agate platform instance you are connecting to.

    :param db_host: the Agate database host name
    :type db_host: str
    :param db_port: the Agate database port
    :type db_port: str
    :param db_name: the Agate database name
    :type db_name: str
    :param agate_username: the client's user name to be used to access Agate resources
    :type agate_username: str
    :param agate_password: the client's password to be used to access Agate resources. If None, Azure device flow will be used for authentication.
    :type agate_password: str
    :param tenant_id: the Agate unique tenant identifier in Azure
    :type tenant_id: str
    :param app_client_id: the Agate client application identifier
    :type app_client_id: str
    :param cache_directory: the local directory to be used to cache files downloaded from Agate. It can be an absolute path or relative to the current working directory
    :type cache_directory: str
    :param max_cpus: the maximum number of CPUs to be used by any parallel processing including file download. Defaults to the number of CPU cores available on the machine.
    :type max_cpus: int
    '''
    def __init__(
        self, 
        agate_username: str, 
        db_host: str = None, 
        db_port: str = None, 
        db_name: str = None, 
        tenant_id: str = None,
        app_client_id: str = None,
        functions_base: str = None,
        cache_directory: str = None, 
        agate_password: str = None,
        max_cpus: int = None):

        self.agate_username = agate_username

        if not db_host:
            db_host = "adaptiveagate-db.database.windows.net"

        self.db_host = db_host
        logger.debug(f"db_host={self.db_host}")

        if not db_port:
            db_port = "1433"

        self.db_port = db_port
        logger.debug(f"db_port={self.db_port}")

        if not db_name:
            db_name = "agate"

        self.db_name = db_name
        logger.debug(f"db_name={self.db_name}")

        if not tenant_id:
            tenant_id = "720cf133-4325-491c-b6a9-159d0497fc65"

        self.tenant_id = tenant_id
        logger.debug(f"tenant_id={self.tenant_id}")

        if not app_client_id:
            app_client_id = "fdcf242b-a25b-4b35-aff2-d91d8100225d"

        self.app_client_id = app_client_id
        logger.debug(f"app_client_id={self.app_client_id}")

        if not functions_base:
            functions_base = "https://adaptiveagateuserfunctions.azurewebsites.net"

        self.functions_base = functions_base
        logger.debug(f"functions_base={self.functions_base}")

        if not cache_directory:
            cache_directory = os.path.join(os.path.expanduser("~"), ".agate_data")

        self.cache_directory = cache_directory
        logger.debug(f"cache_directory={self.cache_directory}")

        self.agate_password = agate_password

        if max_cpus:
            self.max_cpus = max_cpus
        else:
            self.max_cpus = multiprocessing.cpu_count()
        logger.debug(f"max_cpus={self.max_cpus}")

    def from_explicit_path(config_path):
        cfg = None
        with open(config_path) as config_file:
            cfg = Config(**json.load(config_file))
        return cfg

    def clone(self):
        return(copy.deepcopy(self))

    __file_config = None
    __file_config_lock = threading.Lock()

    def from_file():
        ''' Loads a Config object from a file named agate_config.json in the current
        directory or the user's home directory.
        '''
        if Config.__file_config == None:
            with Config.__file_config_lock:
                if Config.__file_config == None:
                    Config.__file_config = Config.__parse_file()
        return Config.__file_config

    def __parse_file():
        """
        Parse config file by looking for a file named agate_config.json in the current
        directory followed by the user's home directory.

        :return: Config object containing the relevant config info
        """
        # Find the config path
        config = None
        for loc in os.curdir, os.path.expanduser("~"):
            try:
                with open(os.path.join(loc, "agate_config.json")) as config_path:
                    config = Config(**json.load(config_path))
            except IOError:
                pass

        if config is None:
            raise FileNotFoundError("An agate_config.json was not found in the current directory or in the user's home directory")

        return config



