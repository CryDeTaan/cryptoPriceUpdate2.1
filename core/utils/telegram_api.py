#!/usr/bin/env python

__author__ = 'Christiaan de Wet'

import json
import requests
import urllib
import logging

import config

logger = logging.getLogger(__name__)

# Some variables from and not from the config file.
chat_id = config.telegram_bot['chat_id']
TOKEN = config.telegram_bot['token']

URL = f"https://api.telegram.org/bot{TOKEN}/"


def get_url(url):
    """
        The main function that interacts with the API. We'll do some try/except to make sure that we actually receive
        data from the API before sending back the callback.

        :param url: URL used by either the send_message() or get_message() functions.

        :return: js_content from the API.
    """

    logger.debug(f'Trying Telegram API HTTP connection.')

    # Try making connection, and then raise exception if a non-200 status response was received.
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.debug(f'Telegram API request successful.')
    except requests.exceptions.RequestException:
        logger.debug(f'Telegram API request error occurred')
        return 'Null'

    # TODO: Retry if error occurred.

    # Prepare the response before returning to the calling function.
    content = response.content.decode("utf8")
    js_content = json.loads(content)
    logger.debug(f'Returning Telegram API response to the handler for processing.')
    return js_content


def send_message(text='', chat_id=chat_id):
    """
        Send the message to the Telegram API. These messages will most often than not be initiated by the handler.

        :param text: The text that will be sent to the API
        :param chat_id: The chat ID of where the message should be sent.

        :return: None
    """

    logger.debug(f'Sending message so the Telegram API')
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    response = get_url(url)

    # Check if the message was sent successfully.
    if response == 'Null':
        logger.debug(f'Sending message so the Telegram API failed.')
    else:
        logger.debug(f'Sending message so the Telegram API successful.')


def get_messages(offset=None):
    """
        Gets all the latest messages since the last offset.

        :param offset: Int representing the last message, this is basically what the Telegram API uses to mark
        message as read. Any message with an ID less than the Offset will no longer be accessible via the API.

        :return: json payload used by the handler to process the message.
    """

    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    js_content = get_url(url)
    return js_content
