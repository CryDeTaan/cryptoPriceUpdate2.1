#!/usr/bin/env python

__author__ = 'Christiaan de Wet'

import json
import requests
import logging

logger = logging.getLogger(__name__)

# Setting the API URL as variable.
URL = "https://api.coinmarketcap.com/v1/"


def get_url(url):
    """
        The main function that interacts with the API. We'll do some try/except to make sure that we actually receive
        data from the API before sending back the callback.

        :param url: API URL

       :return: js_content from the API.
    """
    logger.debug(f'Trying CoinMarketCap API connection.')

    # Try making connection, and then raise exception if a non-200 status response was received.
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.debug(f'CoinMarketCap API request successful.')
    except requests.exceptions.RequestException:
        logger.debug(f'Telegram API request error occurred')
        return 'Null'

    # TODO: Retry if error occurred.

    # Prepare the response before returning to the calling function.
    content = response.content.decode("utf8")
    js = json.loads(content)
    logger.debug(f'Returning CoinMarketCap API response to the handler for processing.')
    return js


def get_coin_data(coin):
    """
        Builds the URL based on the coin parameter received and calls the get_url() function

        :param coin: The coin to build the URL for.

        :return: JSON payload as callback to the handler for further processing.
    """
    url = URL + f"ticker/{coin}"
    data = get_url(url)
    return data
