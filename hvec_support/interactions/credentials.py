"""
Get user name and password.

HVEC, 2022
"""


import easygui as gui


def get_credentials(site_name = ""):
    """
    Ask user for credentials of a protected location.
    
    Args:
        None
    
    Return:
        dictionary containing username and password
    """
    cred = {}
    cred['username'] = gui.enterbox(msg = "Enter username", title = f"Accessing {site_name}")
    cred['password'] = gui.enterbox(msg = "Enter password", title = f"Accessing {site_name}")
    return cred
