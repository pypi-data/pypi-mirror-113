from datetime import datetime, date, timedelta
import time
import numpy
import pandas
import os

from olivia_dataset.utilities.config import read_olivia_dataset_config
from olivia_dataset.utilities.web.download import cookie_enabled_download

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def retrieve_us_covid19_cases_using_1point3acres_api() -> None:
    # - retrieving the config
    config = read_olivia_dataset_config()
    point3acres_key = config['keys']['1point3acres']
    livedataset_repo = config['livedataset_repo']

    os.makedirs(os.path.join(livedataset_repo, 'resolution', 'county'), exist_ok=True)
    filepath = os.path.join(livedataset_repo, 'resolution', 'county', 'cases.csv')

    # - downloading
    cookie_enabled_download(
        url=f'https://instant.1point3acres.com/v1/api/coronavirus/us/cases?token={point3acres_key}',
        output_filepath=filepath
    )

    # - retrieving and performing critical preprocessings
    cases = pandas.read_csv(filepath)
    cases.county_name = cases.county_name.apply(lambda x: x.split('--')[0] if '--' in x else x)
    cases.loc[
        (cases.county_name == 'Wayne--Non Detroit') & (cases.state_name == 'MI'), 'county_name'] = 'Wayne'
    cases.loc[(cases.county_name == 'Wayne--Detroit') & (cases.state_name == 'MI'), 'county_name'] = 'Wayne'
    cases.loc[(cases.county_name == 'Henderon') & (cases.state_name == 'NC'), 'county_name'] = 'Henderson'
    cases = cases.groupby(['confirmed_date', 'county_name', 'state_name']).sum().reset_index()
    cases = cases.loc[:, ['confirmed_date', 'county_name', 'state_name', 'confirmed_count', 'death_count',
                          'recovered_count']]
    cases[(cases['confirmed_date'] == '2020-04-14') & (cases['county_name'] == 'New York') & (
            cases['state_name'] == 'NY') & (cases['death_count'] == 4334)]['death_count'] = 434

    cases.to_csv(filepath)
    logger.info(f"the cases file has been successfully saved into {filepath}")
