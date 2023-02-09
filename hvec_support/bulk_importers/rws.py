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

# Company packages
# We use the rws-package one level below the user interface
from hvec_importers.rws import communicators as rws
from hvec_support import sqlite as hvsq
from hvec_support.bulk_importers import show_progress as prg
from hvec_support.bulk_importers import data_handling as dth


START = '1850-1-1'
END   = '2100-12-31'


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
    global i, N, startTime

    name = selection['Naam'].unique().item()
    quant = selection['Grootheid.Omschrijving'].unique().item()

    logging.info(f'Downloading data of {quant} for {name}')

    i += 1
    prg.show_progress(f'RWS Waterinfo {quant}', name, i, N, startTime)

    # Get data
    df = rws.get_data(selection)

    # Store
    if len(df) > 0:
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
    log_base = 'RWS Waterinfo automatic download'

    stations.reset_index(inplace = True)
    stations['start'] = START
    stations['end']   = END

    # Grouping on code instead of name because we use package hvec_importers one
    # level deeper than the interface
    groups = stations.groupby(by = ['Code', 'Grootheid.Code'], as_index = False)
    groups.apply(lambda x: _get_chunk(x, con = con))
    return
