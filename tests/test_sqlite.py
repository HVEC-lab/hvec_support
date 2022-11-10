"""
Tests for the module sqlite

HVEC, 2022
"""


import pytest as pyt
import pandas as pd
import sqlite3 as sq

from hvec_support import sqlite as hvsq


def test_store_with_columns_check():

    data = {'Name': ['Arthur', 'Merlin', 'Lancelot'], 'Age': [62, 87, 46]}
    df1 = pd.DataFrame(data)

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
