import json
import os


def read_olivia_dataset_config():
    assert os.path.isfile(os.path.abspath(os.path.join(os.path.expanduser("~"), '.olivia_dataset', 'config.json'))), "please configure the oliviadataset package first."
    with open(os.path.abspath(os.path.join(os.path.expanduser("~"), '.olivia_dataset', 'config.json')), 'r') as handle:
        config = json.load(handle)
    return config