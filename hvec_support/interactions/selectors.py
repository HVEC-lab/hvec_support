"""
Collection of selectors.

HVEC lab, 2022
"""

import os
import logging
import sqlite3 as sq
import easygui as gui

from hvec_support import sqlite as hvsq


def select_locations(stationList, title = ''):
    """
    From a list of locations provided on input, manually select a set for further processing.

    Parameters
    ----
    stationList: dataframe with location information
    title: string to show as window title
    """
    choices = stationList['name'].tolist()

    selection = gui.multchoicebox(
        title = title, msg = "Choose locations (more than one allowed)", choices = choices)

    res = stationList.query('name == @selection')

    return res


def get_inputspecs_sq():
    """
    Specify data selection from a database in sqlite.
    """

    logging.info('Interaction with user')
    # Choose file
    out = {}
    out['file'] = gui.fileopenbox(msg = 'Data is expected to be in sqlite. Select your input file',
                            default = os.getenv('DATAPATH'),
                            filetypes = ['*.db', '*.sqlite', 'db', '.sqlite'])

    # Connect database and choose table
    cnxn = sq.connect(out['file'], detect_types = True)
    tableList = hvsq.getTableList(cnxn)
    out['table'] = gui.choicebox(
        msg = 'Pick the table containing the data', choices = tableList)

    # Create list of columns and specify column names
    #TODO put in loop
    columnList = hvsq.getColumnList(cnxn, out['table'])
    out['locationColumn'] = gui.choicebox(
        msg = 'Pick the column containing the location', choices = columnList)
    columnList.remove(out['locationColumn'])

    out['timeColumn'] = gui.choicebox(
        msg = 'Pick the column containing the time', choices = columnList)
    columnList.remove(out['timeColumn'])  # Expect every column to be used in one role at most

    out['levelColumn'] = gui.choicebox(
        msg = 'Pick the column containing the level', choices = columnList)
    columnList.remove(out['levelColumn'])

    cnxn.close()

    return out
