# Copyright 2020, Adaptive Biotechnologies
''' Contains the methods used to get Azure authorization tokens for use with the Agate platform. '''
import sys
import msal, atexit, os, threading 
from msal import PublicClientApplication
import time
import traceback
import urllib.parse

from .config import Config

import logging
logger = logging.getLogger(__name__)

''' The resource URL for the Agate Azure SQL Database. '''
SQL_RESOURCE = "https://database.windows.net//.default"

''' The resource URL for the Agate Azure file store. '''
STORAGE_RESOURCE = "https://storage.azure.com//.default"

msalAppCache = {}
msalAppLock = threading.Lock()

def get_access_token_with_config(resource: str, config: Config) -> str:
    ''' Gets an authorization token for the specified resource using the credentials specified in the configuration. 

    :param resource: the resource URL for which to obtain an access token.
    :type resource: str
    :param config: the Config instance containing the user's Agate credentials, and Azure specific identifiers.
    :type config: Config

    :return: the Azure authorization token for the requested resource
    :rtype: str

    :Example:
        auth_token_provider.get_access_token_with_config(
            auth_token_provider.SQL_RESOURCE,
            Config.from_file())

    '''
    return get_access_token(resource, config.agate_username, config.agate_password, config.tenant_id, config.app_client_id)

def get_function_token_with_config(config: Config) -> str:
    ''' Gets an authentication token for the agate user functions using the credentials specified in the configuration. 

    :param config: the Config instance containing the user's Agate credentials, and Azure specific identifiers.
    :type config: Config

    :return: the Azure authentication token for the requested user
    :rtype: str
    '''
    resource = urllib.parse.urljoin(config.functions_base, "/user_impersonation")
    return get_access_token(resource, config.agate_username, config.agate_password, config.tenant_id, config.app_client_id)

def get_access_token(resource: str, username: str, password: str, tenant_id: str, app_client_id: str) -> str:
    ''' Gets an authorization for the specified resource using the specified credentials.

    :param resource: the resource URL for which to obtain an access token.
    :type resource: str
    :param username: the Agate user name to authenticate with
    :type username: str
    :param password: the Agate user password to authenticate with. If None, Azure device flow authentication will be used.
    :type password: str
    :param tenant_id: the unique Agate Azure tenant identifier
    :type tenant_id: str
    :param app_client_id: the unique Agate client identifier
    :type app_client_id: str

    :return: the Azure authorization token for the requested resource
    :rtype: str
    '''

    with msalAppLock:
        return __get_access_token(resource, username, password, tenant_id, app_client_id)

def __get_access_token(resource: str, username: str, password: str, tenant_id: str, app_client_id: str) -> str:

    token = __get_cached_token(resource, username, password, tenant_id, app_client_id)
    
    result = None
    if token and "access_token" in token:
        result = token["access_token"]
    elif token:
        message = "{}: {}".format(token.get("error"), token.get("error_description"))
        logger.error(message)
        raise Exception(message)

    return result

def __get_cached_token(resource: str, username: str, password: str, tenant_id: str, app_client_id: str) -> str:
    app = __get_cached_app(tenant_id, app_client_id)

    token = None
    accounts = app.get_accounts(username)
    if accounts:
        logger.debug("Account exists in app cache. Getting token silently.")
        account = accounts[0]
        token = app.acquire_token_silent([resource], account)

    if not token:
        if not password:
            logger.debug("Account doesn't exist in app cache or failed to acquire token silently. Proceeding through device flow.")
            flow = app.initiate_device_flow([resource])
            print("Enter code " + flow["user_code"] + " at https://www.microsoft.com/devicelogin to proceed...")
            token = app.acquire_token_by_device_flow(flow)
        else:
            logger.debug("Account doesn't exist in app cache or failed to acquire token silently. Proceeding through username/password flow.")
            token = app.acquire_token_by_username_password(username, password, [resource])

    return token


def __get_cached_app(tenant_id: str, app_client_id: str):
    authority = "https://login.microsoftonline.com/{}".format(tenant_id)

    # super-hacky ... for test, return a brand new app with no token cache
    # every time to be sure that caching behavior doesn't screw us up.
    if (str(sys.argv).find("unittest") != -1 or str(sys.argv).find("pytest") != -1):
        return PublicClientApplication(app_client_id, authority=authority)

    key = tenant_id + "_" + app_client_id

    if not key in msalAppCache:

        cacheFile = os.path.expanduser("~/.agate_" + key + ".bin")
        cache = msal.SerializableTokenCache()

        if os.path.exists(cacheFile):
            with open(cacheFile, "r") as f:
                cache.deserialize(f.read())

        atexit.register(lambda:
            open(cacheFile, "w").write(cache.serialize())
            if cache.has_state_changed else None
            )

        app = PublicClientApplication(app_client_id, authority=authority, token_cache=cache)
        msalAppCache[key] = app

    return msalAppCache[key]
        

