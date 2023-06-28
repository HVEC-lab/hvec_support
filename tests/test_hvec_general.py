"""
Tests for sub-package hvec_styles.

HVEC, April 2022
"""


import os
import hvec_support.general as general
import pytest as pyt

@pyt.mark.parametrize('lng', ['', 'Dutch', 'English'])
def test_show_rundate(lng):
    general.show_rundate(lng)
    return


@pyt.mark.parametrize('project_name', ['9999_010 - client - test project'])
def test_set_project_folder(project_name):
    """
    Test changing work directory using only project number
    """
    project_number = project_name[0:8]
    BASE = f'{os.getenv("ONEDRIVECOMMERCIAL")}/20 werk/'
    
    os.chdir(BASE)
    os.mkdir(f'{BASE}{project_name}')

    general.set_project_folder(project_number)

    assert project_number in os.getcwd()
    
    os.chdir('..')
    os.rmdir(f'{BASE}{project_name}')
    return
