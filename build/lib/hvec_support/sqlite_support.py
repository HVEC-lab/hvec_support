"""
Module containing functions supporting the use of sqlite  
"""

# Import general packages
import sqlite3 as sq
import pandas as pd

# In[210]: Generate range of datetime

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


def intervals(start, end, freq_in = 'Y'):
    """
    Create intervals of dates for import using methods contained in Pandas.

    Start date rounded down to the beginning of the interval and the end date
    rounded up to the end of the interval to prevent missing data.
    """
    startrange = pd.date_range(
        start + pd.offsets.MonthBegin(0),
        end + pd.offsets.MonthEnd(0),
        freq = freq_in + 'S').to_series().dt.to_pydatetime()
    endrange = pd.date_range(
        start + pd.offsets.MonthBegin(0),
        end + pd.offsets.MonthEnd(0),
        freq= freq_in).to_series().dt.to_pydatetime()
    if len(startrange) > len(endrange):
        final_date = dt.datetime.today() - dt.timedelta(days = 1)
        final_date = final_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        endrange = np.concatenate((endrange, [final_date]))
    return list(zip(startrange, endrange))
    

def connect(conn_str):
    """ 
    Convenience method. Connect database and show available tables.
    Verbose version of sq.connect

    Args:
        conn_str, string: connection string (file name with path)

    Returns:
        cnxn, connection object: database connector
    """
    cnxn = sq.connect(conn_str)
    
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
        "DELETE FROM " + table +
        "WHERE rowid NOT IN ( "
            "SELECT MIN(rowid) " 
            "FROM " + table + 
            "GROUP BY %s" %columns
            )    
    
    cnxn.execute(sql, cnxn)
    cnxn.execute("VACUUM")
    return
        