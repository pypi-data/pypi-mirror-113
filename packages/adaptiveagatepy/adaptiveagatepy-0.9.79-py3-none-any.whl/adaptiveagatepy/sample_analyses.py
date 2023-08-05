# Copyright 2020, Adaptive Biotechnologies
''' Contains APIs for interacting with Agate Sample Analysis APIs. '''

from typing import List, Mapping
from datetime import datetime
from io import StringIO
import urllib.parse
import requests
import pandas
import time
import traceback

from . import azure_token_provider
from .config import Config

import logging
logger = logging.getLogger(__name__)

def top(config: Config, 
            sample_name: str,
            max_count: int = 500,
            raw: bool = False):
    ''' Returns most abundant rearrangements from a sample
    
    :param config: the configuration object from which Agate user credentials resource urls are provided.
    :type config: Config
    :param sample_name: sample to query (name or id)
    :type sample_name: str
    :param max_count: number of rearrangement rows to return (max 2,500)
    :type max_count: int
    :param raw: False to return a Pandas DataFrame, true to return a TSV string with headers
    :type raw: bool

    :return: Pandas DataFrame (or TSV string with headers if raw = True)
    '''
    if not config: raise ValueError("config must be provided.")
    if not sample_name: raise ValueError("sample_name must be provided.")
    if not max_count: raise ValueError("max_count must be provided.")

    start_time = time.time()

    try:
        params = {
            "sample": sample_name,
            "count": max_count,
            "footer": False }

        return(__functions_get(config, "/api/Top", params, raw))

    except Exception as e:
        logger.error('Failed in call to sample_analyses.top. ' + traceback.format_exc())
        raise

    finally:
        logger.info("Top completed in %s seconds." % (time.time() - start_time) )

def search(config: Config, 
            sample_names: List[str], 
            search_string: str,
            sequence_type: str = "bioidentity", 
            match_type: str = "exact",
            aligned_cdr3_index: int = 0,
            aligned_muts_allowed: int = 0,
            raw: bool = False):
    ''' Searches for a sequence within a set of samples
    
    :param config: the configuration object from which Agate user credentials resource urls are provided.
    :type config: Config
    :param sample_names: the samples in which to search (max 100 samples)
    :type sample_names: List[str]
    :param search_string: The sequence to search for
    :type search_string: str
    :param sequence_type: The sequence type to search (bioidentity, productive_rearrangement, all_rearrangement, amino_acid)
    :type sequence_type: str
    :param match_type: The match algorithm to use (exact, substring, jside, aligned) (FIXME: need more details here)
    :type match_type: str
    :param aligned_cdr3_index: only for aligned search, index of j-side edge of CDR3 in search_string
    :type aligned_cdr3_index: int
    :param aligned_muts_allowed: only for aligned search, number of substitutions allowed
    :type aligned_muts_allowed: int
    :param raw: False to return a Pandas DataFrame, true to return a TSV string with headers
    :type raw: bool

    :return: Pandas DataFrame (or TSV string with headers if raw = True)
    '''
    if not config: raise ValueError("config must be provided.")
    if not sample_names: raise ValueError("sample_names must be provided.")
    if len(sample_names) == 0: raise ValueError("sample_names must not be empty.")
    if not search_string: raise ValueError("search_string must be provided.")
    if not sequence_type: raise ValueError("sequence_type must be provided.")
    if not match_type: raise ValueError("match_type must be provided.")
        
    if (match_type == "aligned"):
        if not aligned_cdr3_index: raise ValueError("aligned_cdr3_index must be provided for aligned search.")


    start_time = time.time()

    try:
        params = {
            "samples": ",".join(sample_names), 
            "search": search_string,
            "sequenceType": sequence_type,
            "matchType": match_type,
            "alignedCdr3Index": aligned_cdr3_index,
            "alignedMutationsAllowed": aligned_muts_allowed }

        return(__functions_get(config, "/api/Search", params, raw))
    
    except Exception as e:
        logger.error('Failed in call to sample_analyses.search. ' + traceback.format_exc())
        raise

    finally:
        logger.info("Search completed in %s seconds." % (time.time() - start_time) )

def overlap(config: Config, 
            sample_names: List[str], 
            sequence_type: str = "bioidentity", 
            metric_type: str = "frequency",
            min_overlap: int = 2,
            pivot: bool = False,
            raw: bool = False):
    ''' Computes the overlap between a set of samples
    
    :param config: the configuration object from which Agate user credentials resource urls are provided.
    :type config: Config
    :param sample_names: the sample set to overlap (max 100 samples)
    :type sample_names: List[str]
    :param sequence_type: The sequence type to compare (bioidentity, productive_rearrangement, all_rearrangement, amino_acid)
    :type sequence_type: str
    :param metric_type: The metric to aggregate and report (frequency, template, reads)
    :type metric_type: str
    :param min_overlap: the minimum number of samples that must contain a sequence
    :type min_overlap: int
    :param pivot: False to report one line per sequence/sample, True to report each sample in a column
    :type pivot: bool
    :param raw: False to return a Pandas DataFrame, true to return a TSV string with headers
    :type raw: bool

    :return: Pandas DataFrame (or TSV string with headers if raw = True)
    '''
    if not config: raise ValueError("config must be provided.")
    if not sample_names: raise ValueError("sample_names must be provided.")
    if len(sample_names) < 2: raise ValueError("at least two sample_names must be provided.")
    if not sequence_type: raise ValueError("sequence_type must be provided.")
    if not metric_type: raise ValueError("metric_type must be provided.")
    if not min_overlap: raise ValueError("min_overlap must be provided.")
    if min_overlap < 2: raise ValueError("min_overlap must be >= 2.")
    if min_overlap > len(sample_names): raise ValueError("min_overlap must be <= the number of samples provided.")

    start_time = time.time()

    try:
        params = {
            "samples": ",".join(sample_names),
            "sequenceType": sequence_type,
            "metricType": metric_type,
            "minOverlap": min_overlap,
            "pivot": pivot }

        return(__functions_get(config, "/api/Overlap", params, raw))
    
    except Exception as e:
        logger.error('Failed in call to sample_analyses.overlap. ' + traceback.format_exc())
        raise

    finally:
        logger.info("Overlap completed in %s seconds." % (time.time() - start_time) )

def __functions_get(config, relative_url, params, raw):
    url = urllib.parse.urljoin(config.functions_base, relative_url)
    access_token = azure_token_provider.get_function_token_with_config(config)
    headers = { 'Authorization': "Bearer {}".format(access_token), 'x-ms-date': __format_utc_time() }

    response = requests.get(url, headers=headers, params=params)

    if not response.ok: 
        raise RuntimeError(f"Error response {response.status_code} from {url} with message: {response.text}")

    body = response.text

    if not body: 
        raise RuntimeError(f"No content returned from {url}")

    if raw: 
        return body

    return pandas.read_csv(StringIO(body), sep="\t")
    
def __format_utc_time():
    return datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

