"""
Tests for map creation

HVEC-lab, 2023
"""


import pandas as pd


from hvec_support import maps


test = pd.DataFrame(data = {
      'name': 'OLV-toren Amersfoort'
    , 'x': 155
    , 'y' 463
    , 'stelsel': '25831'
})


def test_map_creation():
    print(test)
    return