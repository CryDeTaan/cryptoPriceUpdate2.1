#!/usr/bin/env python

__author__ = 'Christiaan de Wet'

from core.utils.coinmarketcap_api import get_coin_data


class Coin:
    def __init__(self, coin):
        self.coin = get_coin_data(coin)
        self.name = self.coin[0]['name']
        self.price_usd = "$" + self.coin[0]['price_usd']
        self.percent_change_1h = self.coin[0]['percent_change_1h']
        self.percent_change_24h = self.coin[0]['percent_change_24h']
        self.percent_change_7d = self.coin[0]['percent_change_7d']

    def __str__(self):
        return f'{self.name}:\n' + \
            f'{self.price_usd}\n' + \
            f'1h change: {self.percent_change_1h:>6}%\n' + \
            f'24h change: {self.percent_change_24h:>5}%\n' + \
            f'7d change: {self.percent_change_7d:>5}%\n'
