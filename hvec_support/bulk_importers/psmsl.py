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
from hvec_support.bulk_importers import user_interaction as usr
from hvec_support.bulk_importers import data_handling as dth


def bulk_import(con, stations, freq = 'annual', include_metric = False):
    """
    Booster importing all PSMSL data. Metric data optional.
    """
    #TODO set logging to standard logging function
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

    # For every id in the station list, obtain the data
    for id in tqdm(stations.index):
        df = pd.DataFrame()
        log = pd.DataFrame()
        
        type = stations.loc[id, 'type']
        name = stations.loc[id, 'name']

        time.sleep(5)
        df = psmsl.data_single_id(id, freq, type)
        log = prepare_log(df, name)

        dth.store_data(con, df)
        dth.write_log(con, log)    
    return df, log