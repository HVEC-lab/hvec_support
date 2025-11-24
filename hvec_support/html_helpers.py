"""
Support working with internet requests.

HVEC-lab, 2025
"""

from bs4 import BeautifulSoup
import requests


def listhtml(url, ext=''):
    """
    Create list of files on a given url.

    Source: https://stackoverflow.com/questions/11023530/python-to-list-http-files-and-directories

    Args:
        url: web-address to check
        ext: file extension (optional)
    
    Returns:
        res: list of filenames
    """
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    res = [
        #url + '/' + 
        node.get('href') 
        for node in soup.find_all('a') 
        if node.get('href').endswith(ext)
        ]
    return res
