"""
Tests for map creation

HVEC-lab, 2023
"""

import os
import pandas as pd
import pytest as pyt
from matplotlib.figure import Figure

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



@pyt.mark.parametrize('margin', [0.01, [0.01, 0.02]])
def test_map_creation_1(margin):
    """
    Test custom map
    """
    map = maps.location_map(df = test, margin = margin, col_spec = specification, color = 'red')
    assert isinstance(map, Figure)

  
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
    assert isinstance(map, Figure)
  