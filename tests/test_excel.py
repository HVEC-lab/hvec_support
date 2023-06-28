"""
Unit tests for Excel-support
"""


import os
import io
import pandas as pd
import hvec_support.excel as hvex


def test_add_graph_to_writer():
    FILE = r'test.xlsx'
    image_file = open(r'logo.png', 'rb')
    image_data = io.BytesIO(image_file.read())
    image_file.close()

    wb = pd.ExcelWriter(FILE)

    hvex.add_graph_to_writer(wb, file = r'logo.png', sheetname = 'test')
    wb.close()
    os.remove(FILE)
    return
