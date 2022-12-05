"""
Unit tests for Excel-support
"""

import io
import pandas as pd
import hvec_support.excel as hvex


def test_add_graph_to_writer():
    image_file = open(r'./tests/logo.png', 'rb')
    image_data = io.BytesIO(image_file.read())
    image_file.close()

    wb = pd.ExcelWriter(r'./tests/test.xlsx')

    hvex.add_graph_to_writer(wb, file = r'./tests/logo.png', sheetname = 'test')
    wb.close()
    return
