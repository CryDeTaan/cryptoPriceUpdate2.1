#!/usr/bin/env python

__author__ = 'Christiaan de Wet'

import json
import requests

URL = "https://api.coinmarketcap.com/v1/"

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    js = json.loads(content)
    return js

def get_coin_data(coin):
    url = URL + f"ticker/{coin}"
    data = get_url(url)
    return data
