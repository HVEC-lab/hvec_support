"""
Tests for map creation

HVEC-lab, 2023
"""


import pandas as pd


from hvec_support import maps


test = pd.DataFrame(data = {
      'Naam': 'OLV-toren Amersfoort'
    , 'X': 155
    , 'Y': 463
    , 'stelsel': '25831'
}, index = [0])


specification = {
      'x': 'X'
    , 'y': 'Y'
    , 'name': 'Naam'
    , 'coordinate_system': 'stelsel'
}


def test_map_creation():
    """
    Test custom map
    """
    map = maps.LabeledMap()#df = test, col_spec = specification)
    #map.show()
    return