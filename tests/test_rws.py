"""
Test suite for bulk importer RWS
"""

from hvec_support.bulk_importers import rws
import pandas as pd
import sqlite3 as sq
import os

os.chdir('./tests')
selection = pd.read_excel(r'RWS_test_selection.xlsx')


def test_bulk_import():
    """
    Test bulk import
    """
    con = sq.connect('Test.db')
    rws.bulk_import(stations = selection, con = con)
    return
