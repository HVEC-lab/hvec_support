"""
Bulk importer for RWS data.

The RWS dataset is extensive. Therefore, this library assumes a shopping list
of parameters and locations to be provided in Excel. 

Storage is assumed to be provided in a database in sqlite.

By storing on disk, we avoid memory overload which is shown to dramatically
slow down the procedure.

HVEC lab, 2023
"""

# Public packages
import logging
import datetime as dt
import dateutil
import requests
import time
from tqdm import tqdm

# Company packages
# We use the rws-package one level below the user interface
from hvec_importers.rws import communicators as rwscom
from hvec_importers.rws import helpers as rwshlp
from hvec_importers.rws import parsers as rwsparse
from hvec_importers.rws.constants import WAIT
from hvec_support import sqlite as hvsq
from hvec_support.bulk_importers import show_progress as prg
from hvec_support.bulk_importers import data_handling as dth


START = '1680-1-1'
END   = '2100-12-31'


def _crude_prune(location, session):
    """
    Limit the used date range based on data availability in
    a crude but rapid procedure
    """
    start = dateutil.parser.parse(location['start'].squeeze())
    end = dateutil.parser.parse(location['end'].squeeze())

    end = min(end, dt.datetime.today())
    location['end'] = end.strftime("%Y-%m-%d")

    interval = end - start
    middle = start + (interval / 2)

    # Check lower half for data
    data_present = rwscom.assert_data_available(location, start, middle, session)
    if data_present:
        return location
    
    # replace start date with middle date and repeat
    location['start'] = middle.strftime("%Y-%m-%d")
    location = _crude_prune(location, session)  # recursive call
    return location


def _get_chunk(selection, con):
    """
    Support function getting and storing a chunk of data
    following a single line in the shopping list.

    This function is to be called from a "groupby" statement
    where we abuse the groupby to select a single row.

    Args:
        name, quantity: location and quantity as strings
        con, database connector object
    """
    # TODO: use the function for importing slices from hvec_importers. Current version imports too large dataframes and is hence too slow
    global i, N, startTime

    log_base = 'RWS Waterinfo automatic download'
    name = selection['Naam'].unique().item()
    quant = selection['Grootheid.Omschrijving'].unique().item()

    logging.info(f'Downloading data of {quant} for {name}')

    i += 1
    prg.show_progress(f'RWS Waterinfo {quant}', name, i, N, startTime)

    # Get data using functions from hvec_importers in such a way that
    # memory use is kept to a minimum
    session = requests.session()

    # Assert date range not empty
    start = dateutil.parser.parse(selection['start'].squeeze())
    end = dateutil.parser.parse(selection['end'].squeeze())
    data_present = rwscom.assert_data_available(selection, start, end, session)
    if not data_present:
        session.close()
        return

    # Set date range, avoiding intervals void of data
    selection = _crude_prune(selection, session)
    date_range = rwshlp.date_series(selection['start'].squeeze(), selection['end'].squeeze())
    date_range = rwscom.prune_date_range(selection, date_range, session)

    for (start_i, end_i) in tqdm(date_range):
        time.sleep(WAIT)
        try:
            raw = rwscom.get_raw_slice(selection, start_i, end_i, session)
            clean = rwsparse.parse_data(raw)
            df = rwsparse.format_data(clean)
        except Exception as e:
            logging.debug(e)
            continue

        # Store data
        dth.store_data(con, df)

        # Write data log
        hvsq.write_log(
            entry = f'{log_base}. Station: {name}; 'f'Number of points: {len(df)}', cnxn = con)
    return


def bulk_import(con, stations):
    """
    Bulk-importer RWS data.
    """
    global i, N, startTime

    logging.info("Bulk importer for RWS Waterinfo invoked")

    i = 0
    N = len(stations)
    startTime = dt.datetime.now()

    stations.reset_index(inplace = True)
    stations['start'] = START
    stations['end']   = END

    # Grouping on code instead of name because we use package hvec_importers one
    # level deeper than the interface
    groups = stations.groupby(by = ['Code', 'Grootheid.Code'], as_index = False)
    groups.apply(lambda x: _get_chunk(x, con = con))
    return
