"""
Data handling for bulk importers.

Part of booster package HVEC. All rights reserved.

HVEC lab, 2022
"""

import os
import logging
import datetime as dt
import pandas as pd


def store_data(cnxn, df):
    """
    Store the data to a seperate table
    """
    logging.info('Storing raw data')

    df.to_sql(name = 'data', con = cnxn, index = True, if_exists = 'append')

    cnxn.commit()
    return
