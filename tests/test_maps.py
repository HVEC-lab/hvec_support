"""
Tests for map creation

HVEC-lab, 2023
"""

import os
import pandas as pd


from hvec_support import maps


test = pd.DataFrame(data = {
      'Naam': 'OLV-toren Amersfoort'
    , 'X': 155000.
    , 'Y': 463000.
    , 'stelsel': '28992'
}, index = [0])


specification = {
      'x': 'X'
    , 'y': 'Y'
    , 'name': 'Naam'
    , 'coordinate_system': 'stelsel'
}


def test_map_creation_1():
    """
    Test custom map
    """
    map = maps.location_map(df = test, col_spec = specification, color = 'red')
    map.show()
    return

  
def test_map_creation_2():
    """
    Create map of RD-net points
    """
    path = r'./tests'
    file = r'RD_kernnet_2021.xlsx'
    file = os.path.join(path, file)
    df = pd.read_excel(file)
    df['stelsel'] = '28992'

    specification = {
      'x': 'RD x [m]'
    , 'y': 'RD y [m]'
    , 'name': 'Benaming'
    , 'coordinate_system': 'stelsel'
}
    map = maps.location_map(df, col_spec = specification, color = 'red', marker = 'x', fontsize = 4)
    map.show()
    return