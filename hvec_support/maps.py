"""
Module containing functions map creation
"""

# Import general packages
from matplotlib import pyplot as plt
import geopandas as gpd
import contextily as cx


def location_map(df, col_spec, margin = 0.01, fontsize = 8, annotate = True, **kwargs):
    """
    Create labeled map from dataframe

    Args:
    df: dataframe with name, x, y and coordinate system of x and y
    specs: dictionary containing column specification with at least the following keys (case sensitive):
      'name', 'x', 'y', 'coordinate_system'
    margin: scalar or two-element list, margin around point cluster in degrees (lat/lon)
    """
    
    # Bring settings to local variables 
    name_col = col_spec['name']
    x_col = col_spec['x']
    y_col = col_spec['y']
    coord_col = col_spec['coordinate_system']

    # Allow map margin to be set either as a scalar (used for x and y) or as
    # an array, list or tuple. If given as scalar, transform to list
    if isinstance(margin, (float, int)):  # Prevent error if margin is given without decimal point
      margin = [margin, margin]

    # Create geopandas dataframe and transform coordinates
    stations = (
        gpd.GeoDataFrame(
              df, geometry = gpd.points_from_xy(df[x_col], df[y_col])
            , crs = df[coord_col].unique().item()))
    stations.to_crs('WGS84', inplace = True)

    x_min = min(stations.geometry.x) - margin[0]
    x_max = max(stations.geometry.x) + margin[0]
    y_min = min(stations.geometry.y) - margin[1]
    y_max = max(stations.geometry.y) + margin[1]

    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    cx.add_basemap(ax, crs = stations.crs.to_string(), source = cx.providers.OpenTopoMap)

    stations.plot(ax = ax, **kwargs)

    if annotate:
      for x, y, label in zip(stations.geometry.x, stations.geometry.y, stations[name_col]):
        ax.annotate(
            label
          , xy = (x, y)
          , xytext = (10, 10)
          , textcoords = 'offset points'
          , backgroundcolor = 'white'
          , fontsize = fontsize)
    return fig
