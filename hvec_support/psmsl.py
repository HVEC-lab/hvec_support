"""
Internal booster functions for PSMSL import. 

Private collection in addition to hvec_importers.psmsl.

HVEC-lab, May 2022
"""


# Public packages
import pandas as pd
import warnings
from tqdm import tqdm

# Company packages
import hvec_importers.psmsl as psmsl


def full_import(freq = 'annual', include_metric = False):
    """
    Booster importing all PSMSL data. Metric data optional.
    """
    if freq == 'annual' and include_metric:
        include_metric = False
        warnings.warn(
            'Metric data only monthly. include_metric set to False'
            )

    # Get station list
    stations = psmsl.station_list(include_metric)
    stations.set_index(keys = 'ID', inplace = True)

    # For every id in the station list, obtain the data
    df = pd.DataFrame()
    
    for id in tqdm(stations.index):
        type = stations.loc[id, 'type']
        tmp = psmsl.data_single_id(id, freq, type)
        df = pd.concat([df, tmp])
    
    return df