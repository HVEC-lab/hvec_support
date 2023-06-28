"""
Test suite for bulk importer RWS
"""


import os
import sqlite3 as sq
import pandas as pd
from hvec_support.bulk_importers import rws


os.chdir('./tests')
selection = pd.read_excel(r'RWS_test_selection.xlsx')


def test_bulk_import():
    """
    Test bulk import
    """
    FILE = 'Test.db'

    con = sq.connect(FILE)
    rws.bulk_import(stations = selection, con = con)

    con.close()
    os.remove(FILE)
    return
