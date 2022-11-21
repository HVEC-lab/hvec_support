from hvec_support.interactions import credentials as cr
import pytest as pyt


def test_get_credentials():
    username, password = cr.get_credentials()
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert len(username) > 0
    assert len(password) > 0