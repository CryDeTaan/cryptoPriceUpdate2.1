#!/usr/bin/env python

__author__ = 'Christiaan de Wet'

import json
import requests
import urllib
import logging


import config

logger = logging.getLogger(__name__)

TOKEN = config.telegram_bot['token']
URL = f"https://api.telegram.org/bot{TOKEN}/"
chat_id = config.telegram_bot['chat_id']


def get_url(url):
    response = requests.get(url)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        logger.debug(f'HTTPError occurred: {e}')
        return 

    # Must have been a 200 status code
    content = response.content.decode("utf8")
    js_content = json.loads(content)
    return js_content


def send_message(text='', chat_id=chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    get_url(url)


def get_messages(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    js_content = get_url(url)
    return js_content
