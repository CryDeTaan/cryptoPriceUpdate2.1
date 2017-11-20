__author__ = 'CryDeTaan'

import schedule
import logging
import time

from core import jobs

logger = logging.getLogger(__name__)


'''
Schedule:
    Every second    - Run the job that listens for new telegram messages.
    Every hour      - Send an update on the bitcoin price.
'''

schedule.every(1).second.do(jobs.listener)

schedule.every(1).hour.do(jobs.updater)


def start_schedule():
    
    """
    This method runs the schedule.
    :return:
    """

    while True:
        schedule.run_pending()
        time.sleep(1)

