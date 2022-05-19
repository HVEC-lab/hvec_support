"""
Module containing functions supporting the use of sqlite  
"""

# Import general packages
import sqlite3 as sq
import pandas as pd
import datetime as dt
import numpy as np
import os


def datetime_range(start, end, delta):
    """
    H.G. Voortman; 15-5-2020

    Taken from 
    https://stackoverflow.com/questions/10688006/generate-a-list-of-datetimes-between-an-interval
    ===============================================================================
    Modified to exporting an array of datetime
    """
    current = start
    out = []
    if not isinstance(delta, dt.timedelta):
        delta = dt.timedelta(**delta)
    while current < end:
        out.append(current)
        current += delta
#        out = np.vstack((out, current))
    return out
    

def connect(conn_str, *args, **kwargs):
    """ 
    Convenience method. Connect database and show available tables.
    Verbose version of sq.connect

    Args:
        conn_str, string: connection string (file name with path)

    Returns:
        cnxn, connection object: database connector
    """
    cnxn = sq.connect(conn_str, *args, **kwargs)
    
    sql = "SELECT name FROM sqlite_master WHERE type == 'table' "
    names = pd.read_sql(sql, cnxn)
    
    print("The database ", conn_str, " is opened.")
    print("This database contains the following tables: ")
    print(names)
    return cnxn


def remove_doubles(cnxn, table, columns):
    """
    Remove double entries in specified table
    and columns.

    Args:
        cnxn, object: database connection
        table, string: target table
        columns, list: columns for which doubles are to be avoided
    """
    sql = (
        "DELETE FROM '" + table + "'"
        " WHERE rowid NOT IN ( "
            "SELECT MIN(rowid) " 
            "FROM '" + table + "' " 
            "GROUP BY " + columns +
            ")")    
    
    cnxn.execute(sql, cnxn)
    cnxn.execute("VACUUM")
    return


def store_data(entity, data, log, **kwargs):
    """
    Storing data to the default HVEC data infrastructure
    """    
    os.chdir(os.getenv('DATAPATH'))

    file = entity + '.db'
    cnxn = sq.connect(file)

    data.to_sql(
        'data', cnxn, **kwargs
        )
    log.to_sql(
        'log', cnxn, **kwargs
        )

    cnxn.close()
    return