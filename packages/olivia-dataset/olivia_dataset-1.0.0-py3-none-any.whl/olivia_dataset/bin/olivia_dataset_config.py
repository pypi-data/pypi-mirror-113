#!/usr/bin/env python
import os
import json

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("welcome to olivia_dataset package.")

    config_repo = os.path.abspath(os.path.join(os.path.expanduser("~"), '.olivia_dataset'))
    os.makedirs(config_repo, exist_ok=True)

    if os.path.isfile(os.path.join(config_repo, "config.json")):
        logger.info(f"the stored configuration is loaded for modification.")
        with open(os.path.join(config_repo, "config.json"), 'r') as handle:
            config = json.load(handle)
    else:
        logger.info(f"the configuration repository is made in {config_repo}")
        config = dict()

    # - preparing the keys if there is none
    if 'keys' not in config.keys():
        config['keys'] = dict()

    # - 1point3acres
    point3acres_key = input("please input the 1point3acres key for retrieving coronavirus data for US.\n\t>> ")
    config['keys']['1point3acres'] = point3acres_key

    # - livedataset path
    livedataset_repo = input("please insert the path to the live dataset repo.\n\t>> ")
    os.makedirs(os.path.abspath(livedataset_repo), exist_ok=True)
    config['livedataset_repo'] = livedataset_repo

    # - dumping the json configuration
    with open(os.path.join(config_repo, "config.json"), 'w') as handle:
        json.dump(config, handle)

    logger.info(f"olivia_dataset package is successfully initialized, and the configuration file is saved into {os.path.join(config_repo, 'config.json')}")
