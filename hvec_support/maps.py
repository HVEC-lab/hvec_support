"""
Module containing functions map creation
"""

# Import general packages
import geopandas as gpd
import contextily as cx


def location_map(df, specs, margin = 0.01, **kwargs):
    """
    Create labeled map from dataframe

    Args:
    df: dataframe with name, x, y and coordinate system of x and y
    specs: dictionary containing column specification
    margin: margin around point cluster in degrees (lat/lon)
    """
    
    # Bring settings to local variables 
    name_col = specs['name']
    x_col = specs['x']
    y_col = specs['y']
    coord_col = specs['coord']

    # Create geopandas dataframe and transform coordinates
    stations = (
        gpd.GeoDataFrame(
              df, geometry = gpd.points_from_xy(df[x_col], df[y_col])
            , crs = df['coord_col'].unique().item()))
    stations.to_crs('WGS84', inplace = True)

    ax = stations.plot(figsize, color)
    ax.set_xlim(min(stations.geometry.x) - margin, max(stations.geometry.x) + margin)
    ax.set_ylim(min(stations.geometry.y) - margin, max(stations.geometry.y) + margin)
    cx.add_basemap(ax, crs = stations.crs.to_string(), source = cx.providers.OpenTopoMap)
    for x, y, label in zip(stations.geometry.x, stations.geometry.y, stations.Code):
        ax.annotate(label, xy = (x, y), xytext = (3, 3), textcoords = 'offset points')
    return
