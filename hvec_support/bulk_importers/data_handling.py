"""
Data handling for bulk importers.

Part of booster package HVEC. All rights reserved.

HVEC lab, 2022
"""

import os
import logging
import datetime as dt
import pandas as pd


def prepare_logLine(info):
    """
    Store log information on current download action to
    a dataframe.

    Parameters
    ------
    info: dictionary with log info
    cnt: number of stored data points
    """
    logline = pd.DataFrame(info, index = [0])
    logline['downloaded'] = dt.datetime.today().strftime('%Y-%m-%d %H:%M')
    logline['source'] = 'Scraped with ' + os.getenv('COMPUTERNAME')
    return logline


def write_log(cnxn, info):
    """
    Update log in database.

    info is a dictionary with log data. Solved in this way, the log info is flexible.
    """
    logline = prepare_logLine(info)
    logline.to_sql(con = cnxn, name = 'log', if_exists = 'append', index = False)

    cnxn.commit()
    return


def store_data(cnxn, df):
    """
    Store the data to a seperate table
    """
    logging.info('Storing raw data')

    df.to_sql(name = 'data', con = cnxn, index = True, if_exists = 'append')

    cnxn.commit()
    return
