import logging
import requests
import time
import json

API_URL = 'https://testnet.bitmex.com/api/v1'


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    # Change this to DEBUG if you want a lot more info
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def load_config():
    json_data = open("config.json").read()
    data = json.loads(json_data)
    return data


def get_instruments():
    r = requests.get(API_URL + '/instrument/active',
                     headers={'Accept': 'application/json'})
    instruments = [instrument.get('symbol') for instrument in r.json()]
    return instruments
