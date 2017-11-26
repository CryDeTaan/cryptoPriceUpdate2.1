__author__ = 'Christiaan de Wet'


class Coin:
    """
        This class is really just here as I wanted to at least use one class in the program as part of the learing.
        probably not even the correct way to use a class, but ¯\_(⊙︿⊙)_/¯
    """
    def __init__(self, coin):
        """
            Setting so manny variables it not even funny.

            :param coin: The coin data payload from the handler which was obtained from the Coin Market Cap API.
        """
        self.coin = coin
        self.name = self.coin[0]['name']
        self.price_usd = "$" + self.coin[0]['price_usd']
        self.percent_change_1h = self.coin[0]['percent_change_1h']
        self.percent_change_24h = self.coin[0]['percent_change_24h']
        self.percent_change_7d = self.coin[0]['percent_change_7d']

    def __str__(self):
        """
            Specifically wanted to use this builtin method so that when the Coin class is called a using a str function.

            :return: Formatted srt ready for delivery.
        """
        return f'{self.name}:\n' + \
            f'{self.price_usd}\n' + \
            f'1h change: {self.percent_change_1h:>6}%\n' + \
            f'24h change: {self.percent_change_24h:>5}%\n' + \
            f'7d change: {self.percent_change_7d:>5}%\n'
