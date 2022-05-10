"""
Package bringing several supporting functions together.

Created by HVEC, the practical knowledge provider, 2022
"""
from .admin import __author__, __author_email__, __version__

"""
The module excelsupport contains a collection of functions
boosting the use of Excel for reporting.
"""
from . import excel_support

"""
The module sqlitesupport contains a collection of functions
boosting the use of sqlite for large files.
"""
from . import sqlite_support

"""
The module hvec_styles contains style definitions
for HVEC reporting
"""
from . import hvec_styles