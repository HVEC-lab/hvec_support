"""
Tests for html helpers.

HVEC-lab, 2025
"""

import sys
import pytest as pyt

from hvec_support import html_helpers as hthlp

@pyt.mark.parametrize(
          'url, ext'
        , [
              ('https://stackoverflow.com', '')
            , ( 'https://knmi.nl', '')])

def test_listhtml(url, ext):
    res = hthlp.listhtml(url, ext)
    assert len(res) > 0
