"""
Module containing functions map creation
"""

# Import general packages
from matplotlib import pyplot as plt
import geopandas as gpd
import contextily as cx


def location_map(df, col_spec, xytext, margin = 0.01, fontsize = 8, **kwargs):
    """
    Create labeled map from dataframe

    Args:
    df: dataframe with name, x, y and coordinate system of x and y
    specs: dictionary containing column specification
    margin: margin around point cluster in degrees (lat/lon)
    """
    
    # Bring settings to local variables 
    name_col = col_spec['name']
    x_col = col_spec['x']
    y_col = col_spec['y']
    coord_col = col_spec['coordinate_system']

    # Create geopandas dataframe and transform coordinates
    stations = (
        gpd.GeoDataFrame(
              df, geometry = gpd.points_from_xy(df[x_col], df[y_col])
            , crs = df[coord_col].unique().item()))
    stations.to_crs('WGS84', inplace = True)

    x_min = min(stations.geometry.x) - margin
    x_max = max(stations.geometry.x) + margin
    y_min = min(stations.geometry.y) - margin
    y_max = max(stations.geometry.y) + margin

    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    cx.add_basemap(ax, crs = stations.crs.to_string(), source = cx.providers.OpenTopoMap)

    stations.plot(ax = ax, **kwargs)
    for x, y, xytxt, label in zip(stations.geometry.x, stations.geometry.y, xytext, stations[name_col]):
        ax.annotate(
                label
              , xy = xytxt
              , xytext = (10, 10)
              , textcoords = 'offset points'
              , backgroundcolor = 'white'
              , fontsize = fontsize)
    return fig
