__author__ = "CryDeTaan"

import time
import logging
from collections import Counter
from re import search as re_search

import config
from core.utils import coinmarketcap_api
from core.utils import telegram_api
from core.utils import prepare_string_response_for_coin


logger = logging.getLogger(__name__)

# Some variables from and not from the config file.
coin_list = config.telegram_bot['coin_list']

ban_dict = {}
recent_sender_dict = {}
last_message_id = None


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
    global last_message_id

    '''
        Using the API get the unread messages, and if there are any new messages send them to the handler where most of the
        processing will happen. This function really just acts as a gateway.
    '''
    messages = telegram_api.get_messages(last_message_id)

    '''
        Only process the response if the correct data was received. if not log result attribute missing.
    '''
    logger.debug(f'Checking Telegram API response.')
    if 'result' in messages and len(messages['result']) > 0:
        last_message_id = get_last_message_id(messages) + 1
        handle_messages(messages)

    logger.debug(f'Message result attribute missing.')


def updater():
    """
        Get the price of the set coins in the config file from coinmarketcap API and send telegram on an hourly basis.

    :return: None
    """

    for coin in coin_list:
        coin = coinmarketcap_api.get_coin_data(coin)

        # Check if the coin variable contains any of the expected data.
        if 'name' in coin[0]:
            logger.debug(f'Setting up response for sending message to Telegram API.')
            coin_string = str(prepare_string_response_for_coin.Coin(coin))
            telegram_api.send_message(text=coin_string)
        continue


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
        The function updates this dictionary outside of it's scope as we only care about the dictionary from another
        function. This might not be the best way of doing it, but ¯\_(ツ)_/¯

        :param messages: messages['date'] and message['from']['first_name']

        :return: None
    """

    # This dictionary will be used to send a message to all the users that has just been banned.
    banned_users = []

    '''
        use Counter from the collections module to count the occurrences of the messages sent by a user. Save this to a
        dictionary that will be iterated over to determine if any used has sent multiple messages in a single getUpdates
        API call to the telegram API. 
    '''
    try:
        messages_count = dict(Counter([item['message']['from']['first_name'] for item in messages['result']]))
    except KeyError:
        logger.debug(f'Oh shit, lets hope this does not happen often. No banning can occur this time around.')

    '''
        Calculate if sender should be banned. If the same sender count is more than on in one get_updates, we can 
        already assume that more than 1 message has been sent in 5 seconds and therefore will be banned for 5 minutes.
    '''
    for from_name, message_count in messages_count.items():
        if message_count > 2:
            ban_dict[from_name] = time.time() + 300
            banned_users.append(from_name)
            logger.debug(f'{from_name} has been banned for 5 min')

    '''
        Calculate if sender should be banned. If the same sender sends more than two message is 5 seconds,
        they will be banned for 5 minutes.
        
        If the user is not banned, either by the previous step or this step, we still want to note the time so that we 
        can calculate if we've seen a message from the same user in the last 5 seconds, 
        which is what happens in the else section.
    '''
    sender_time = {message['message']['from']['first_name']: message['message']['date'] for message in
                   messages['result']}
    for from_name in sender_time:
        if from_name in recent_sender_dict:
            if (recent_sender_dict[from_name] + 5) > sender_time[from_name]:
                ban_dict[from_name] = time.time() + 300
                banned_users.append(from_name)
                logger.debug(f'{from_name} has been banned for 5 min')
        else:
            recent_sender_dict[from_name] = time.time()
            logger.debug(f'{from_name} has been added to the recent_sender_dict')

    # If the ban list is empty, there is no reason to run this part of the code, so we first check if we need to.
    if len(banned_users) > 0:
        text = "NO! Don't do that " + \
               ', '.join(str(banned_user) for banned_user in banned_users) + \
               ", I am ignoring you for 5 min! "
        telegram_api.send_message(text)

    # TODO: Clear the ban_dict = {} after a certain period.


def handle_messages(messages):
    """
        A few checks need to happen on all incoming message.
        1. Set some variables.
        2. Check if the text in the message might be a command which starts with a '/'.
        3. Check if the sender has been banned because of sending to many consecutive messages or in quick succession.
        4. If the message starts with / and matches one of the commands, get update for coin and send to telegram chat.
        :param messages: All received messages since the last getUpdates()
        :return:
    """

    # Some variables to use during this function call.
    update_ban_list(messages)
    coins_to_update = []

    # For each message we need to perform a few operations.
    logger.debug(f'Handling messages.')
    for message in messages["result"]:

        try:
            # Set variables that will be used for each message.
            first_name = message['message']['from']['first_name']
            message_time = message['message']['date']
            message_text = message['message']['text']

        except KeyError:
            logger.debug(f'Not a message that needs to be handled.')
            continue

        # Check if sender is banned, if sender is in ban list move to next message.
        if first_name in ban_dict and message_time < ban_dict[first_name]:
            logger.debug(f'A banned sender tried to send a message.')
            continue

        '''
            This try/except will check if a received message is considered to be a command because the message stars
            with a /, it will also save the command as a variable called coin.
            If the message does not start with / it will not be a command and the loop can continue to the next message.
        '''
        try:
            search_coin = re_search("(?<=^/)[a-z]+", message_text)
            coin = search_coin.group()
            logger.debug(f'The message received maybe a command as it starts with /.')
        except AttributeError:
            logger.debug(f'The message received is not a command, no / found.')
            continue

        '''
            Check if the /command matches any of the following:
            1. bitcoincash, reason for this check is because the command option from the telegram @botfather does not
            allow "-" in the name, and breaks, so we need to specifically check for this and then add the correct coin
            as required by the Coin Market Cap API which is bitcoin-cash
            2. all, if the command matches all, we will loop over all the coins in the coin_list and append it to a new
            list which we will used at the end to collect all the coins data from the Coin Market Cap API
            3. <coin>, lastly if the command matches any of the coins in the coin_list, the coin will be added to the 
            coins_to_update variable.
        '''
        logger.debug(f'Checking if the coin command variable matches any of the expected coins.')
        if 'coin' in locals():
            if coin == 'bitcoincash':
                coins_to_update.append('bitcoin-cash')

            elif coin == 'all':
                for coin in coin_list:
                    coins_to_update.append(coin)

            elif coin in coin_list:
                coins_to_update.append(coin)

    '''
        Now that we have a list of all the coins from the latest messages we can loop over them to collect the coin data
        from the Coin Market Cap API and send it to the Telegram API to deliver to the chat_id. 
        We also check if the response form the Coin Market Cap API returned any results. 
    '''
    for coin_to_update in coins_to_update:
        coin = coinmarketcap_api.get_coin_data(coin_to_update)

        # Check if the coin variable contains any of the expected data.
        if 'name' in coin[0]:
            logger.debug(f'Setting up response for sending message to Telegram API.')
            coin_string = str(prepare_string_response_for_coin.Coin(coin))
            telegram_api.send_message(text=coin_string)

        logger.debug(f'No response received from the Coin Market Cap API.')
        continue


