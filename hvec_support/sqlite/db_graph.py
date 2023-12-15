"""
Graphically presented info about database.

HVEC-lab, 2023
"""


from hvec_support.sqlite import db_info
from matplotlib import pyplot as plt
import seaborn as sns


def availability_graph(table, con, index, columns, values):
    """
    Show heat plot of data availability

    Args:
        table: table name
        cnxn: database connection
        index, columns, values: settings for pivot table
    
    Output:
        Graph object
    """

    df = db_info.availability_table(table, con, index, columns, values)

    ax = sns.heatmap(df, cmap = 'coolwarm')

    for sp in ax.spines:
        ax.spines[sp].set_visible(True)
    
    ax.set_xlabel(columns)

    return ax
