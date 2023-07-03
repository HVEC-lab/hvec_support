"""
Collection of selectors.

Part of hvec_support/interactions

HVEC lab, 2022
"""

import os
import logging
import sqlite3 as sq
import easygui as gui

from hvec_support import sqlite as hvsq


def select_locations(stationList, title = '', col_name = 'name'):
    """
    From a list of locations provided on input, manually select a set for further processing.

    Parameters
    ----
    stationList: dataframe with location information
    title: string to show as window title
    """
    choices = stationList[col_name].unique().tolist()
    choices.sort()

    selection = gui.multchoicebox(
        title = title, msg = "Choose locations (more than one allowed)", choices = choices)

    mask = stationList[col_name].isin(selection)
    return stationList[mask]


def get_inputspecs_field_data():
    """
    Specify data selection from a database with field data in sqlite.
    """

    logging.info('Interaction with user getting selection of field data')
    # Choose file
    out = {}
    out['file'] = gui.fileopenbox(msg = 'Data is expected to be in sqlite. Select your input file',
                            default = os.getenv('DATAPATH'),
                            filetypes = ['*.db', '*.sqlite', 'db', '.sqlite'])

    # Connect database and choose table
    cnxn = sq.connect(out['file'], detect_types = False)
    tableList = hvsq.getTableList(cnxn)

    out['locationTable'] = gui.choicebox(
        msg = 'Pick the table containing metadata of the locations', choices = tableList
    )
    tableList.remove(out['locationTable'])  # Prevent double selection of table

    out['dataTable'] = gui.choicebox(
        msg = 'Pick the table containing the data', choices = tableList)

    # Create list of columns and specify column names
    #TODO put in loop
    columnList = hvsq.getColumnList(cnxn, out['dataTable'])
    out['locationColumn'] = gui.choicebox(
        msg = 'Pick the column containing the unique location identifier', choices = columnList)
    columnList.remove(out['locationColumn'])

    out['nameColumn'] = gui.choicebox(
        msg = 'Pick the column containing the location name', choices = columnList)
    columnList.remove(out['nameColumn'])

    out['timeColumn'] = gui.choicebox(
        msg = 'Pick the column containing the time', choices = columnList)
    columnList.remove(out['timeColumn'])  # Expect every column to be used in one role at most

    out['levelColumn'] = gui.choicebox(
        msg = 'Pick the column containing the level', choices = columnList)
    columnList.remove(out['levelColumn'])

    cnxn.close()  # Prevent side effects by closing database connection

    return out
