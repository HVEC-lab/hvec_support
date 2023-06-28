"""
Test suite for bulk importer RWS
"""


import os
import sqlite3 as sq
import pandas as pd
import pytest as pyt
from hvec_support.bulk_importers import rws


os.chdir('./tests')
selection = pd.read_excel(r'RWS_test_selection.xlsx')

@pyt.mark.parametrize(
    "start, end, expected_size", [
        ('1-1-1950', '1-1-1954', 3002368),
        ('1-1-1850', '31-12-1855', 0),
        ('15-12-1975', '15-2-1976', 364544)
    ])
def test_bulk_import(start, end, expected_size):
    """
    Test bulk import
    """
    FILE = 'Test.db'

    con = sq.connect(FILE)
    rws.bulk_import(stations = selection, con = con)

    con.close()
    os.remove(FILE)
    return
