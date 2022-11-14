"""
Internal booster functions for IPCC import. 

Private collection in addition to hvec_importers.psmsl.

HVEC-lab, May 2022
"""


# Public packages
import pandas as pd
from tqdm import tqdm
import datetime as dt
import os
import time

# Company packages
import hvec_importers.ipcc as ipcc
import hvec_importers.psmsl as psmsl


def bulk_import():
    """
    Booster importing all IPCC sea level scenarios.
    """
    def prepare_log(df, name):
        """
        Register every individual import action
        """
        logline = pd.DataFrame()
        logline['name'] = [name]
        logline['downloaded'] = dt.datetime.today().strftime('%Y-%m-%d %H:%M')
        logline['source'] = 'Scraped with ' + os.getenv('COMPUTERNAME')
        logline['number of points'] = len(df)
        return logline

    # Get station list from PSMSL
    stations = psmsl.station_list(include_metric = True)
    stations.set_index(keys = 'ID', inplace = True, drop = True)

    # For every id in the station list, obtain the data
    df = pd.DataFrame()
    log = pd.DataFrame()
    
    for id in tqdm(stations.index):
        name = stations.loc[id, 'Station Name']

        time.sleep(2)
        tmp = ipcc.data_single_id(id)
        tmp['name'] = name

        logline = prepare_log(tmp, name)

        if len(tmp) > 0:
            df = pd.concat([df, tmp])
        log = pd.concat([log, logline])    
    return df, log