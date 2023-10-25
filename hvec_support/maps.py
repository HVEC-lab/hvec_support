"""
Module containing functions map creation
"""

# Import general packages
import geopandas as gpd
import contextily as cx


class labeled_map:
    """
    Map from a table with location name, coordinates and coordinate system
    used. This function transforms the coordinates to a geopandas dataframe, transforms
    the coordinates to WGS 84 and plots the points on a map created with contextily
    
    Args:
    df: pandas dataframe with coordinates, name and coordinate system
    col_spec: dictionary specifying the column names
    source: contextily source to be used for the map
    map_limit: spacing around the point cloud in lat/lon degrees
    """
    def __init__(self, df, col_spec, source = cx.providers.OpenTopoMap, map_limit = 0.02):
        x_col = col_spec['x']
        y_col = col_spec['y']
        name_col = col_spec['name']
        print(name_col)
