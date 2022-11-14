"""
Interacting with the user
"""

import os
import logging
import datetime as dt
import numpy as np


def show_progress(source, name, i, total, startTime):
    """
    Show brief progress report to screen
    """
    logging.info(f'Downloading station {name} from {source}')
    current_time = dt.datetime.now()
    deltat_taken = (current_time - startTime).total_seconds() / 60 # total time in minutes
    deltat_remaining = (deltat_taken / i) * (total - i)  # estimate of remaining time in minutes

    os.system('cls')
    print(f'Running import for {source} data')
    print('Time since start: ', np.round(deltat_taken), ' minutes')
    print('Estimated time to finish: ', np.round(deltat_remaining), ' minutes')
    print('Current station: ' + name)
    print('This is station', i, ' of ', total)
    return
