"""
General support module HVEC 
"""

import os
import logging
import datetime as dt
import locale as loc
import matplotlib.pyplot as plt

# In[15] Set plot format
SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 24
VERY_BIG    = 32

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=VERY_BIG)     # fontsize of the figure title


def show_rundate(lng = 'English'):
    if lng == 'English':
        print("This sheet was run at: ", dt.datetime.today().strftime('%d %B %Y'))
    elif lng == 'Dutch':
        loc.setlocale(loc.LC_TIME, 'nl_NL.utf8')
        print("Deze sheet werd gerund op: ", dt.datetime.today().strftime('%d %B %Y'))
    return


def set_project_folder(project_number):
    """
    Change working directory to the project folder based on the
    HVEC project number
    """
    BASE = f'{os.getenv("ONEDRIVE")}/20 werk/'
    os.chdir(BASE)

    names = os.listdir()

    for nm in names:
        if nm.startswith(project_number):
            os.chdir(nm)
            return
  
    raise ValueError(f'Project {project_number} not found')


def show_progress(program, msg):
    """
    Show progress information
    """
    os.system('cls')
    print(f"Currently running {program}")
    print(msg)
    logging.info(msg)
    return
