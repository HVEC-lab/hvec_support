"""
Package bringing several supporting functions together.

Created by HVEC, the practical knowledge provider, 2022
"""
from .admin import __author__, __author_email__, __version__

from . import excel
from . import sqlite
from . import styles

from .bulk_importers import ipcc
from .bulk_importers import psmsl
from .bulk_importers import rws
from .bulk_importers import knmi
from .bulk_importers import gloss
