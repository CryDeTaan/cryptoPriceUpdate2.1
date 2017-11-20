__author__ = "CryDeTaan"

import time
import logging
from collections import Counter
from re import search as re_search

from core.utils import telegram_api
from core.utils import coins

logger = logging.getLogger(__name__)

ban_dict = {}
recent_sender_dict = {}


def listener():
    """
        The listener listens to any messages to the bot, privately or in a group.
        These messages are then handled by the different handlers.
        Its acts as the gateway between the APIs and the utilities.
        :return:
    """

    '''
        Need to keep track of the message id, which is used as an offset in the telegram API, so that the messages 
        before this offset are basically marked as read and will no longer be available to the bot.
        We will update this ID during the while loop.
    '''
    last_message_id = None

    '''
        Using the API get the unread messages, and if there are any new messages send them to the handler where most of the
        processing will happen. This function really just acts as a gateway.
    '''
    while True:
        messages = telegram_api.get_messages(last_message_id)

        if len(messages["result"]) > 0:
            last_message_id = get_last_message_id(messages) + 1
            handle_messages(messages)

        time.sleep(0.5)


def updater():
    """
        Get the price of the give coins from coinmarketcap API and send telegram on an hourly basis.

    :return:
    """

    coin_list = ['bitcoin', 'neo', 'bitcoin-cash']

    for coin in coin_list:
        coin_update = str(coins.Coin(coin))
        telegram_api.send_message(text=coin_update)



def get_last_message_id(messages):

    """
        Get the last message ID that will be used as an offset for the telegram API, the offset is used to basically mark
        message as read, and all previous messages will forgotten.

        :param messages: a list of messages received by the bot.

        :return: An integer for the last 'update_id' parameter from the given messages
    """

    messages_ids = []

    for message in messages["result"]:
        messages_ids.append(int(message["update_id"]))

    return max(messages_ids)


def update_ban_list(messages):
    """

        Check if the sender has sent two commands in the last 5 seconds or multiple messages in API getUpdates
        call, if so ban for 5 min and notify the user they have been banned for 5 min.

        :param messages: messages['date'] and message['from']['first_name']

        :return: None
    """

    banned_users = []

    '''
        use Counter from the collections module to count the occurrences of the messages sent by a user. Save this to a
        dictionary that will be iterated over to determine if any used has sent multiple messages in a single getUpdates
        API call to the telegram API. 
    '''

    messages_count = dict(Counter([item['message']['from']['first_name'] for item in messages['result']]))

    for from_name, message_count in messages_count.items():
        if message_count > 2:
            ban_dict[from_name] = time.time() + 300
            banned_users.append(from_name)

            logger.debug(f'{from_name} has been banned for 5 min')

    sender_time = {message['message']['from']['first_name']: message['message']['date'] for message in messages['result']}

    for from_name in sender_time:
        if from_name in recent_sender_dict:
            if (recent_sender_dict[from_name] + 5) > sender_time[from_name]:
                ban_dict[from_name] = time.time() + 300
                banned_users.append(from_name)

                logger.debug(f'{from_name} has been banned for 5 min')

        else:
            recent_sender_dict[from_name] = time.time()
            logger.debug(f'{from_name} has been added to the recent_sender_dict')

    if len(banned_users) > 0:
        text = "NO! Don't do that " + \
               ', '.join(str(banned_user) for banned_user in banned_users) + \
               ", I am ignoring you for 5 min! "
        telegram_api.send_message(text)


def handle_messages(messages):
    """

        :param messages:
        :return:
    """

    update_ban_list(messages)

    for message in messages["result"]:

        first_name = message['message']['from']['first_name']
        message_time = message['message']['date']
        message_text = message['message']['text']

        coin_list = ['bitcoin', 'neo', 'bitcoin-cash']

        search_coin = re_search("(?<=^/)[a-z]+", message_text)
        coin = search_coin.group()

        if first_name in ban_dict and message_time < ban_dict[first_name]:
            print('Banned')

        elif coin in coin_list:
            coin_update = str(coins.Coin(coin))
            telegram_api.send_message(text=coin_update)

        elif coin == 'bitcoincash':
            coin_update = str(coins.Coin('bitcoin-cash'))
            telegram_api.send_message(text=coin_update)

        elif coin == 'all':
            for coin in coin_list:
                coin_update = str(coins.Coin(coin))
                telegram_api.send_message(text=coin_update)


