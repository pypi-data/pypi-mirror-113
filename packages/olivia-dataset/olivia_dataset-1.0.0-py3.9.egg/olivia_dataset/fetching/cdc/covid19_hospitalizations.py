from datetime import datetime, date, timedelta
import time
import numpy
import pandas
import os
import json

from olivia_dataset.utilities.config import read_olivia_dataset_config

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def retrieve_cdc_covid19_hospitalizations() -> None:
    """
    Retrieving and preprocessing the CDC data from [https://gis.cdc.gov/grasp/covidnet/COVID19_5.html](https://gis.cdc.gov/grasp/covidnet/COVID19_5.html).
    """
    # - retrieving the config
    config = read_olivia_dataset_config()
    livedataset_repo = config['livedataset_repo']

    cache_folder = os.path.abspath(os.path.join(os.path.expanduser("~"), '.olivia_dataset'))
    os.makedirs(cache_folder, exist_ok=True)

    os.makedirs(os.path.join(livedataset_repo, 'resolution', 'state', 'cdc_covid/covid_hospitalizations'), exist_ok=True)
    filepath = os.path.join(livedataset_repo, 'resolution',  'state', 'cdc_covid/covid_hospitalizations', 'all_covid19_hospitalizations.csv')

    os.system("""
    curl 'https://gis.cdc.gov/grasp/covid19_3_api/PostPhase03DataTool' \
      -H 'authority: gis.cdc.gov' \
      -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
      -H 'accept: application/json, text/plain, */*' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36' \
      -H 'content-type: application/json;charset=UTF-8' \
      -H 'origin: https://gis.cdc.gov' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-mode: cors' \
      -H 'sec-fetch-dest: empty' \
      -H 'referer: https://gis.cdc.gov/grasp/covidnet/COVID19_3.html' \
      -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
      -H 'cookie: s_fid=1C93F28D0A1FCCE8-3035E413E6388A70; s_cc=true; TS01fffff8=015d0abe87d01b0abd95773a7beb71a0736c8b11edb95869efdae8398d8fa5f5c28b94efeca7211a2f298b2a60db323c3fc806c009; gpv_c54=https%3A%2F%2Fgis.cdc.gov%2Fgrasp%2Fcovidnet%2FCOVID19_3.html; s_vncm=1627801199082%26vn%3D2; s_ivc=true; s_lv_s=Less%20than%201%20day; s_visit=1; s_ips=1292; gpv_v45=COVID-19%20Hospitalizations; s_sq=%5B%5BB%5D%5D; RT="z=1&dm=cdc.gov&si=jt2l7aorinh&ss=kra0vsee&sl=0&tt=0"; s_ptc=0.00%5E%5E0.01%5E%5E0.27%5E%5E0.46%5E%5E0.21%5E%5E0.01%5E%5E0.60%5E%5E0.01%5E%5E1.58; s_tp=2035; s_ppv=COVID-19%2520Hospitalizations%2C65%2C63%2C1317%2C1%2C1; arp_scroll_position=38; s_tps=11; s_pvs=10; s_lv=1626667256020' \
      --data-raw '{"appversion":"Public","key":"datadownload","injson":[]}' \
      --compressed""" + f""" > {os.path.join(cache_folder, 'cdc_hospitalization.json')}
      """)

    with open(os.path.join(cache_folder, 'cdc_hospitalization.json'), 'r') as handle:
        data = json.load(handle)
    df = pandas.DataFrame(data['datadownload'])
    df.dropna(inplace=True)

    df.rename({
        'mmwr-week': 'MMWR-WEEK',
        'mmwr-year': 'MMWR-YEAR',
        'age_category': 'AGE CATEGORY',
        'catchment': 'CATCHMENT',
        'weekly-rate': 'WEEKLY RATE ',
        'cumulative-rate': 'CUMULATIVE RATE',
        'network': 'NETWORK',
        'year': 'YEAR',
        'sex_category': 'SEX',
        'race_category': 'RACE'
    }, axis=1, inplace=True)

    df.to_csv(filepath)
    logger.info(f"the cdc covid hospitalizations file has been successfully saved into {filepath}")


def retrieve_cdc_influenza_surveys() -> None:
    """
    Retrieving and preprocessing the CDC data from [https://gis.cdc.gov/grasp/covidnet/COVID19_5.html](https://gis.cdc.gov/grasp/covidnet/COVID19_1.html).
    """
    # - retrieving the config
    config = read_olivia_dataset_config()
    livedataset_repo = config['livedataset_repo']

    cache_folder = os.path.abspath(os.path.join(os.path.expanduser("~"), '.olivia_dataset'))
    os.makedirs(cache_folder, exist_ok=True)

    os.makedirs(os.path.join(livedataset_repo, 'resolution', 'state', 'cdc_covid/weekly_influenza_surveillance'), exist_ok=True)
    filepath = os.path.join(livedataset_repo, 'resolution',  'state', 'cdc_covid/weekly_influenza_surveillance', 'influenza_survey.csv')

    os.system("""
    curl 'https://gis.cdc.gov/grasp/covid19_1_api/Phase1DownloadDataP/60,59,1' \
  -H 'authority: gis.cdc.gov' \
  -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://gis.cdc.gov/grasp/covidnet/COVID19_1.html' \
  -H 'accept-language: en-US,en;q=0.9,fa;q=0.8' \
  -H 'cookie: s_fid=1C93F28D0A1FCCE8-3035E413E6388A70; s_cc=true; s_vncm=1627801199082%26vn%3D2; s_ivc=true; s_lv_s=Less%20than%201%20day; s_visit=1; s_ips=1279; arp_scroll_position=0; s_sq=%5B%5BB%5D%5D; TS01fffff8=015d0abe87d3498655bd8cae5167a43d0070f2e12dd2af8698e99c1b5fc367fcad3772f8337e6b1200df9ec256670c3bd8a542ef49; gpv_v45=COVID-Net%20State%20Activity%20Indicator%20Map; gpv_c54=https%3A%2F%2Fgis.cdc.gov%2Fgrasp%2Fcovidnet%2FCOVID19_1.html%23a50; RT="z=1&dm=cdc.gov&si=65zuw9kllki&ss=kra0vsee&sl=0&tt=0"; s_ptc=0.00%5E%5E0.00%5E%5E0.00%5E%5E0.00%5E%5E0.06%5E%5E0.01%5E%5E0.32%5E%5E0.01%5E%5E0.41; s_tp=1683; s_ppv=COVID-Net%2520State%2520Activity%2520Indicator%2520Map%2C76%2C76%2C1279%2C1%2C1; s_tps=68; s_pvs=1178; s_lv=1626668480844' \
  --compressed """ + f""" > {os.path.join(cache_folder, 'influenza_surveys.json')}
      """)

    with open(os.path.join(cache_folder, 'influenza_surveys.json'), 'r') as handle:
        data = json.loads(json.load(handle))

    df = pandas.DataFrame(data['datadownload'])
    df.dropna(inplace=True)

    df.rename({
        'statename': 'STATENAME',
        'activity_level': 'ACTIVITY LEVEL',
        'weeknumber': 'WEEK',
        'url': 'URL',
        'weekend': 'WEEKEND',
        'website': 'WEBSITE',
        'season': 'SEASON'
    }, axis=1, inplace=True)

    df.to_csv(filepath)
    logger.info(f"the cdc covid hospitalizations file has been successfully saved into {filepath}")