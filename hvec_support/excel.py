"""
Package containing functions to boost the combination of
scripts and excel.  
"""

# In[10] Modules
import os
import openpyxl as xl
import pandas as pd


def import_excel_files(names):
    """
    Import multiple Excel files in a single dataframe.

    Args:
    names: list of file names including path

    Returns:
    df: dataframe with all imported data
    """
    # Create empty results dataframe
    df = pd.DataFrame()

    for nm in names:

        # Read current file
        tmp = pd.read_excel(nm)

        # Combine with earlier data
        df = pd.concat([df, tmp])
    
    return df


# In[100] Formatting Excel files
def set_column_width(worksheet):
    """
    Code taken from
    https://stackoverflow.com/questions/17326973/is-there-a-way-
    to-auto-adjust-excel-column-widths-with-pandas-excelwriter
    worksheet = wrt.sheets[sheetname]  # pull worksheet object
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
            )) + 3  # adding a little extra space
        worksheet.set_column(idx, idx, max_len)  # set column width
    return
    """
    column_widths = []
    for row in worksheet.iter_rows():
        for i, cell in enumerate(row):
            try:
                column_widths[i] = max(column_widths[i], len(str(cell.value)))
            except IndexError:
                column_widths.append(len(str(cell.value)))

    for i, column_width in enumerate(column_widths):
        worksheet.column_dimensions[
            xl.utils.get_column_letter(i + 1)].width = column_width + 3
    return


def format_sheet(worksheet):
    """
    Set worksheet to single page landscape
    """
    pgs = worksheet.page_setup
    pgs.orientation = worksheet.ORIENTATION_LANDSCAPE
    pgs.paperSize = worksheet.PAPERSIZE_A4
    #pgs.fitToHeight = True
    #pgs.fitToWidth = True
    pgs.fitToPage = True
    return


def set_column_width_writer(writer_object):
    """
    Set column widths of all sheets in an excel writer object
    """
    for sh in writer_object.sheets:
        worksheet = writer_object.sheets[sh]
        set_column_width(worksheet)
    return


def add_graph_to_writer(writer_object, file, sheetname):
    """
    Create new sheet and put a graph on it
    """
    pd.DataFrame().to_excel(writer_object, sheet_name = sheetname)
    worksheet = writer_object.sheets[sheetname]
    img = xl.drawing.image.Image(file)
    #img.anchor('A1')
    worksheet.add_image(img)
    return
