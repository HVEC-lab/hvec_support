"""
Collection of selectors.

HVEC lab, 2022
"""

import easygui as gui


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
