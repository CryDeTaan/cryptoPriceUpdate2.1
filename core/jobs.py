__author__ = 'CryDeTaan'

import logging

from core import handler

logger = logging.getLogger(__name__)


def listener():
    """
    Listens for new message to the bot and hands the messages off to the handler.
    :return:
    """

    handler.listener()


def updater():
    """
    Update job that runs the update handler based on a schedule.
    :return:
    """

    handler.updater() 

