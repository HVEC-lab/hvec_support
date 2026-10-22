"""
Unit tests for Excel-support
"""


import os
import io
from pathlib import Path
import pandas as pd
import hvec_support.excel as hvex

TESTS = Path(__file__).parent


def test_add_graph_to_writer():
    FILE = TESTS / 'test.xlsx'
    image_file = open(TESTS / 'Logo.png', 'rb')
    image_data = io.BytesIO(image_file.read())
    image_file.close()

    wb = pd.ExcelWriter(FILE)

    hvex.add_graph_to_writer(wb, file = TESTS / 'Logo.png', sheetname = 'test')
    wb.close()
    os.remove(FILE)
    return
