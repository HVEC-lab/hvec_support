"""
Tests for the module sqlite

HVEC, 2022
"""

import os
import pytest as pyt
import pandas as pd
import sqlite3 as sq

from hvec_support import sqlite as hvsq


data = {'Name': ['Arthur', 'Merlin', 'Lancelot'], 'Age': [62, 87, 46]}
df1 = pd.DataFrame(data)


def test_store_with_columns_check():
    data = {'Name': 'Guinevere', 'Role': 'Princess'} # Never ask a lady her age
    df2 = pd.DataFrame(data, index = [0])

    df_expected = pd.concat([df1, df2])
    df_expected.reset_index(drop = True, inplace = True)

    cnxn = sq.connect(':memory:')

    df1.to_sql('test', if_exists = 'append', con = cnxn, index = False)
    hvsq.store_with_column_check(df2, 'test', cnxn, index = False)

    df = pd.read_sql('SELECT * FROM test', cnxn)
    
    #df.reset_index(drop = True, inplace = True)

    assert df.equals(df_expected)


def test_table_to_csv():
    FILE = r'test.db'

    cnxn = sq.connect(FILE)
    df1.to_sql('test', cnxn, index = False, if_exists = 'replace')
    cnxn.close()

    hvsq.table_to_csv('test', FILE)

    os.chdir(os.path.splitext(FILE)[0])
    assert os.path.exists(r'test.csv')

    os.remove(r'test.csv')
    os.chdir('..')
    os.rmdir(r'./test')
    os.remove(FILE)

    return


def test_db_to_csv():
    FILE = 'test.db'
    BASE = os.getcwd()

    cnxn = sq.connect(FILE)

    tables = ['test1', 'test2', 'test3']

    for tbl in tables:
        df1.to_sql(tbl, cnxn)  # Database with three tables
    cnxn.close()

    hvsq.db_to_csv(FILE)
    os.remove(FILE)

    folder = os.path.splitext(FILE)[0]

    os.chdir(folder)

    for tbl in tables:
        file = f'{tbl}.csv'
        assert os.path.exists(file)
        os.remove(file)
    
    os.chdir(BASE)
    os.rmdir(folder)
    return