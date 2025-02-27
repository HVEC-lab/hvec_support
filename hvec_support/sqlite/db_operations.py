"""
Sub-module of sqlite; operations on a database

HVEC-lab, 2023
"""

# Import general packages
import os
import logging
import datetime as dt
import sqlite3 as sq
import pandas as pd

from hvec_support.sqlite import db_info


def connect_verbose(conn_str, *args, **kwargs):
    """ 
    Convenience method. Connect existing database and show available tables.
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


def initialise(name, replace = True, **kwargs):
    """
    Initialise a database. If an old version exists, it is deleted.
    Subsequently the database connection is opened and returned.
    """
    logging.info('Initialise database')

    if replace:
        logging.info('Deleting existing database is chosen')
        try:
            os.remove(name)
        except FileNotFoundError:
            logging.info('No existing file found.')

    return sq.connect(name, **kwargs)


def readData(settings, **kwargs):
    """
    Read time series from database.

    Parameters
    ----------
    settings: dictionary with at least the fields 'file' and 'dataTable'
    """
    #logging.info(f'Read data from {settings['table']} in {settings['file']}')

    # Connect
    cnxn = sq.connect(settings['file'], **kwargs)

    # Create query 
    table = settings['dataTable']

    keys = ['locationColumn', 'nameColumn', 'timeColumn', 'levelColumn']
    columns = [settings.get(key) for key in keys]
    var_string = ', '.join(columns)

    sql = f"SELECT {var_string} FROM {table}"

    # Read data
    data = pd.read_sql(sql, cnxn)

    # Cleanup and close database connection
    data.dropna(how = 'any', inplace = True)
    cnxn.close()

    return data


def prepare_logLine(entry):
    """
    Store log information on current download action to
    a dataframe.

    Parameters
    ------
    entry: string with log info
    cnt: number of stored data points
    """
    date = dt.datetime.today().strftime('%Y-%m-%d %H:%M')
    machine = os.getenv('COMPUTERNAME')

    cols = ['date', 'log_entry', 'machine']
    line = dict(zip(cols, [date, entry, machine]))
    logline = pd.DataFrame(line, index = [0])
    return logline


def write_log(entry, cnxn):
    """
    Update log in database.

    entry is a string.
    """
    logline = prepare_logLine(entry)
    logline.to_sql(con = cnxn, name = 'log', if_exists = 'append', index = False)

    cnxn.commit()
    return


def remove_doubles(cnxn, table, columns):
    """
    Remove double entries in specified table
    and columns.

    Args:
        cnxn, object: database connection
        table, string: target table
        columns, list: columns for which doubles are to be avoided
    """
    col_string = ', '.join(columns)
    subSql = f"SELECT MAX(rowid) FROM {table} GROUP BY {col_string}"  # Select last entry
    sql = f"DELETE FROM {table} WHERE rowid NOT IN ({subSql})"

    cnxn.execute(sql)
    cnxn.commit()
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


#TODO create a tailor-made dataframe object
def store_with_column_check(df, table, cnxn, **kwargs):
    """
    1. Get columns in the database
    2. Compare to columns in the results dataframe
    3. Add columns if necessary
    4. Store dataframe to database
    """
    logging.info('Storing table with added possibly extra columns')

    if db_info.table_exists(table, cnxn):
        # Check for missing columns
        sql = f"PRAGMA table_info({table})"
        cols_db = pd.read_sql(sql, cnxn)['name'].tolist()
        cols_res = df.columns.tolist()
        missing_columns = list(set(cols_res) - set(cols_db))

        # Add missing columns
        for col in missing_columns:
            logging.info('')
            sql = f'ALTER TABLE {table} ADD "%s" '%col
            cnxn.execute(sql)

    df.to_sql(name = table, con = cnxn, if_exists = 'append', **kwargs)
    cnxn.commit()
    return


def table_to_csv(table, db_file):
    """
    Integral export of selected table to csv
    """
    BASE  = os.getcwd()
    folder = os.path.splitext(db_file)[0]
    sql = f'SELECT * FROM {table}'
    csv_file = f'{table}.csv'

    cnxn = sq.connect(db_file)

    if not os.path.exists(folder):  # When storing multiple tables, only create folder once
        os.mkdir(folder)

    os.chdir(folder)
    
    if os.path.exists(csv_file):
        os.remove(csv_file)  # Remove previous version, if present

    header = True
    mode = "w"
    for df in pd.read_sql(sql, cnxn, chunksize = 100000):
        df.to_csv(csv_file, mode = mode, header = header, index = False)
        if header:
            header = False
            mode = "a"

    # Return files to initial state
    os.chdir(BASE)
    cnxn.close()
    return


def db_to_csv(db_file):
    """
    Copy all tables in a database to csv

    Args:
        db_file: database file name
    """
    cnxn = sq.connect(db_file)
    table_list = db_info.getTableList(cnxn)
    cnxn.close()
    
    for tbl in table_list:
        table_to_csv(tbl, db_file)
    return
 