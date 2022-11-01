"""
Internal booster functions for PSMSL import. 

Private collection in addition to hvec_importers.psmsl.

HVEC-lab, May 2022
"""


# Public packages
import logging
import datetime as dt
import time
import requests

# Company packages
from hvec_importers import psmsl
from hvec_support.bulk_importers import show_progress as prg
from hvec_support.bulk_importers import data_handling as dth


def bulk_import(con, stations):
    """
    Booster importing all PSMSL data. Metric data optional.
    """
    freqs = ['annual', 'monthly']

    startTime = dt.datetime.now()
    session = requests.session()

    for freq in freqs:

        # For every id in the station list, obtain the data
        for i, nr in enumerate(stations.index):

            tp = stations.loc[nr, 'type']
            name = stations.loc[nr, 'name']

            prg.show_progress(f'PSMSL {freq}, {tp}', name, i + 1, len(stations), startTime)

            df = psmsl.data_single_id(nr, session, freq, tp)
            df['name'] = name

            dth.store_data(con, df)
            dth.write_log(
                con, {'dataset': 'psmsl', 'id': nr, 'name': name, 'number of points': len(df)})

    session.close()
    return
