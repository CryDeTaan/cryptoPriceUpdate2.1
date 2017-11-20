#!/usr/bin/env python

__author__ = 'Christiaan de Wet'

import time
import json
import requests
import urllib

import config

TOKEN = config.telegram_bot['token']
URL = f"https://api.telegram.org/bot{TOKEN}/"
chat_id = config.telegram_bot['chat_id']


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    js_content = json.loads(content)
    return js_content


def send_message(text='', chat_id=chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}&ForceReply=False"
    get_url(url)


def get_messages(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    js_content = get_url(url)
    return js_content
