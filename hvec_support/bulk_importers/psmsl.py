"""
Internal booster functions for PSMSL import. 

Private collection in addition to hvec_importers.psmsl.

HVEC-lab, May 2022
"""


# Public packages
import pandas as pd
import warnings
from tqdm import tqdm
import datetime as dt
import os
import time

# Company packages
import hvec_importers.psmsl as psmsl


def bulk_import(freq = 'annual', include_metric = False):
    """
    Booster importing all PSMSL data. Metric data optional.
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


    if freq == 'annual' and include_metric:
        include_metric = False
        warnings.warn(
            'Metric data only monthly. include_metric set to False'
            )

    # Get station list
    stations = psmsl.station_list(include_metric)
    stations.set_index(keys = 'ID', inplace = True, drop = True)

    # For every id in the station list, obtain the data
    df = pd.DataFrame()
    log = pd.DataFrame()
    
    for id in tqdm(stations.index):
        type = stations.loc[id, 'type']
        name = stations.loc[id, 'name']

        time.sleep(5)
        tmp = psmsl.data_single_id(id, freq, type)
        logline = prepare_log(tmp, name)

        if len(tmp) > 0:
            df = pd.concat([df, tmp])
        log = pd.concat([log, logline])    
    return df, log