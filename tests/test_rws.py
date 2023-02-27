"""
Test suite for bulk importer RWS
"""

import os
import pytest as pyt
from hvec_support.bulk_importers import rws
import pandas as pd
import sqlite3 as sq


os.chdir('./tests')

@pyt.mark.parametrize(
    "start, end, expected_size", [
        ('1-1-1950', '1-1-1954', 2605056),
        ('1-1-1850', '31-12-1855', 0),
        ('15-12-1975', '15-2-1976', 364544)
    ])
def test_bulk_import(start, end, expected_size):
    """
    Test bulk import
    """
    selection = pd.read_excel(r'RWS_test_selection.xlsx')
    con = sq.connect('Test.db')

    # Limit the dowload date range to save time
    rws.bulk_import(stations = selection, con = con, start = start, end = end)
    con.close()

    size = os.path.getsize('test.db')
    os.remove('test.db')
    assert size == expected_size
