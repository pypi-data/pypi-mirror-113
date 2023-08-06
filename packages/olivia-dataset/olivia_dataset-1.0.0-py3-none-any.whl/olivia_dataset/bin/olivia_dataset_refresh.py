#!/usr/bin/env python
import argparse
import os
import sys
sys.path.append('/Users/mednet_machine/PHOENIX/ai_health_informatics/pandemic_modeling/olivia_dataset')
import json
import pandas

from olivia_dataset.fetching.cdc import retrieve_cdc_covid19_hospitalizations, retrieve_cdc_influenza_surveys
from olivia_dataset.fetching.covid19_outcomes import retrieve_us_covid19_cases_using_1point3acres_api

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("refreshing the live dataset...")

    config_repo = os.path.abspath(os.path.join(os.path.expanduser("~"), '.olivia_dataset'))
    assert os.path.isfile(os.path.join(config_repo, "config.json")), "no configuration"
    with open(os.path.join(config_repo, "config.json"), 'r') as handle:
        config = json.load(handle)

    try:
        livedataset_repo = config['livedataset_repo']
        assert os.path.isdir(livedataset_repo)
    except Exception as e:
        raise Exception(f"bad configuration -> error details: {e}")

    logger.info(">> [update in progress]: CDC Influenza Surveys")
    retrieve_cdc_influenza_surveys()

    logger.info(">> [update in progress]: CDC Laboratory confirmed COVID-19 Associated Hospitalizations")
    retrieve_cdc_covid19_hospitalizations()

    logger.info(">> [update in progress]: COVID-19 occurrences across the United States")
    retrieve_us_covid19_cases_using_1point3acres_api()

    if os.path.isfile(os.path.join(livedataset_repo, "resolution/county/google_mobility_raw.csv")):
        logger.info(">> [update in progress]: Google community reports on mobility categories")
        df = pandas.read_csv(os.path.join(livedataset_repo, "resolution/county/google_mobility_raw.csv"))
        df = df[df['country_region_code'] == 'US']
        df.drop(columns=['metro_area', 'iso_3166_2_code', 'census_fips_code', 'place_id'], inplace=True)
        df.dropna(inplace=True)
        df.to_csv(os.path.join(livedataset_repo, "resolution/county/google_mobility.csv"))
        c = 'y'  #input("delete the google_mobility_raw? (y/N)\n\t>>")
        if c in ['y', 'Y']:
            os.system(f'rm {os.path.join(livedataset_repo, "resolution/county/google_mobility_raw.csv")}')
