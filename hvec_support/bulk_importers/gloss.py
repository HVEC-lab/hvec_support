"""
Bulk importer for gloss data.

Booster package HVEC. Private.

HVEC lab, 2022
"""

import logging
import datetime as dt
import requests

from hvec_importers import gloss

from hvec_support.bulk_importers import user_interaction as usr
from hvec_support.bulk_importers import data_handling as dth


def bulk_import(con, stationList):
    """
    Function for bulk import of gloss data. To prevent overloading of the site and
    to prevent memory problems, the data is read one location at a time and stored
    to a database before commencing.

    We choose to always download the "fast delivery" set, containing all avaiable data
    up to today. The dataset contains the date up to which quality control has been
    performed, so the choice to use only research quality data can always be made later.

    Parameters
    ------
    con: database connection object
    locations, dataframe with selected station names
    """
    startTime = dt.datetime.now()
    session = requests.session()
    #TODO: "pythonize" the for loop

    for i, nr in enumerate(stationList.index):

        # Progress information and logging
        name = stationList.loc[nr, 'name']
        usr.show_progress('GLOSS', name, i + 1, len(stationList), startTime)

        # Get data
        df = gloss.data_single_id(nr, session, type = 'fast_delivery', drop_current_year = True)
        if len(df) == 0:
            logging.warning('Empty dataframe found')
            continue

        # Store data, constits and log
        dth.store_data(con, df)
        dth.write_log(con, {'dataset': 'gloss', 'id': nr, 'name': name, 'number of points': len(df)})

    con.close()
    session.close()
    return
