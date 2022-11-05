"""
Tests for sub-package hvec_styles.

HVEC, April 2022
"""


import hvec_support.styles as styles
import pytest as pyt

@pyt.mark.parametrize('lng', ['', 'Dutch', 'English'])
def test_show_rundate(lng):
    styles.show_rundate()
    return
