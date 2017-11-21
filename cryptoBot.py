#!/usr/bin/env python
"""
Main entry point into Crypto Bot
"""

__author__ = 'CryDeTaan'

import logging
import os

from core import scheduler

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.dirname(os.path.realpath(__file__)) + '/log/cryptoBot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

# TODO: Add a banner, its what the cool kids do ;p

if __name__ == '__main__':
    '''
    Run the Crypto Bot and handover to the scheduler
    '''

    # TODO: Add a Daemon, look at https://github.com/serverdensity/python-daemon
    
    logger.debug('Handing over to the scheduler')
    scheduler.start_schedule()

