"""
Unit tests for Excel-support
"""

import os
import io
import pandas as pd
import hvec_support.excel as hvex


def test_add_graph_to_writer():
    path = os.path.dirname(__file__)
    os.chdir(path)
    wb = pd.ExcelWriter(r'test.xlsx')

    hvex.add_graph_to_writer(wb, file = r'logo.png', sheetname = 'test')
    wb.close()
    return
