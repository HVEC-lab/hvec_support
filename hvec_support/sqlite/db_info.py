"""
Sub-module of sqlite; information about a database
HVEC-lab, 2023
"""


import pandas as pd


def getTableList(cnxn):
    """
    Get list of tables in a database.
    Input is a database connection object made with sqlite3
    """
    sql = 'SELECT name from sqlite_master where type= "table"'
    tableList = pd.read_sql(sql, cnxn)['name'].tolist()

    return tableList


def table_exists(table, cnxn):
    """
    Verify the existence of a table in a database

    Args:
        table: string with table name
        cnxn: database connection
    Out:
        Boolean
    """
    sql = f'SELECT name FROM sqlite_master WHERE type = "table" AND name = "{table}"'
    return len(cnxn.execute(sql).fetchall()) == 1


def getColumnList(cnxn, table):
    """
    Get list of columns in a specified table
    """
    sql = "SELECT * FROM '%s' ORDER BY ROWID ASC LIMIT 1"%table
    columnList = pd.read_sql(sql, cnxn).columns.tolist()

    return columnList


def availability_table(table, con, index, columns, values):
    """
    Create dataframe with counted entries

    Args:
        table: table name
        cnxn: database connection
        index, columns, values: settings for pivot table
    
    Output:
        Dataframe
    """
    sql = (
        f"SELECT {index}, {columns}, COUNT({values}) AS cnt FROM {table} "
        f"GROUP BY {index}, {columns}"
    )
    df = pd.read_sql(sql, con)
    df = df.pivot(index = index, columns = columns, values = 'cnt')
    return df

