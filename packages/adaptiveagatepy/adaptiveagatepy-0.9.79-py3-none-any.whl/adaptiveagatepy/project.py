# Copyright 2020, Adaptive Biotechnologies
''' Contains higher-level APIs for working with Agate files. '''

from contextlib import closing
from typing import List, Mapping

from . import config 
from . import file
from . import related_files
from .related_files import RelatedFile

def get_files(config: config.Config, project_names: str or List[str], keys: str or List[str], version = related_files.INCLUDE_CURRENT) -> Mapping[str, RelatedFile]:
    ''' For a set of projects, ensures files are in the cache and return local paths

    :param config: the configuration object 
    :type config: Config
    :param project_names: a single or list of project names
    :type project_names: str or List[str]
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

    if (not project_names):
        raise ValueError("project_names must be provided.")

    if (not keys):
        raise ValueError("keys must be provided.")

    return file.__get_files_for_column(config, ["all_projects", "all_anonymized_projects"], "name", project_names, keys, version)
