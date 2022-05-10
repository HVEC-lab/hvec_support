"""
Package containing functions to boost the combination of
scripts and excel.  
"""

# In[10] Modules
import openpyxl as xl

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


def set_column_width_writer(writer_object):
    """
    Set column widths of all sheets in an excel writer object
    """
    for sh in writer_object.sheets:
        worksheet = writer_object.sheets[sh]
        set_column_width(worksheet)
    return