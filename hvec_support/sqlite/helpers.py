"""
Helper functions for sub-module sqlite

HVEC-lab, 2023
"""


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
