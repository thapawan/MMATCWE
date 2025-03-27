import numpy as np
import pandas as pd
import rasterio
from skimage.measure import label, regionprops
from skimage.morphology import medial_axis
from shapely.geometry import LineString, mapping
import geopandas as gpd

def process_raster_medial_axis(raster_path, spatial_resolution=10, crs_epsg=32616):
    """
    Processes a raster image to compute medial axis, width, and geographic coordinates.

    Args:
        raster_path (str): Path to the raster image.
        spatial_resolution (int): Spatial resolution of the raster in meters.
        crs_epsg (int): EPSG code for the coordinate reference system.

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame containing centerline geometry,
                               width, longitude, latitude, and label.
    """
    with rasterio.open(raster_path) as ds:
        img = ds.read(1)
        transform = ds.transform

    img = img > 0
    labels = label(img)

    centerline_data = []
    width_data = []

    for region in regionprops(labels):
        skeleton, distances = medial_axis(region.image, return_distance=True)

        if skeleton.sum() > 1:
            centerline_coords = np.column_stack(np.where(skeleton))
            centerline_coords_geo = [transform * (y, x) for x, y in centerline_coords]
            centerline = LineString(centerline_coords_geo)

            width_pixels = distances[skeleton].max()
            width_meters = width_pixels * spatial_resolution

            centerline_data.append({'Label': region.label, 'geometry': centerline})
            width_data.append({'Label': region.label, 'Width': width_meters})
        else:
            print(f"Skipping region {region.label} due to insufficient skeleton points.")

    df_centerline = pd.DataFrame(centerline_data)
    df_width = pd.DataFrame(width_data)
    merged_df = pd.merge(df_centerline, df_width, on='Label')
    gdf_centerline = gpd.GeoDataFrame(merged_df, geometry='geometry')
    gdf_centerline.set_crs(epsg=crs_epsg, inplace=True)
    gdf_centerline['Longitude'] = gdf_centerline['geometry'].apply(lambda geom: geom.centroid.x)
    gdf_centerline['Latitude'] = gdf_centerline['geometry'].apply(lambda geom: geom.centroid.y)
    gdf_centerline = gdf_centerline[['Longitude', 'Latitude', 'Width', 'Label', 'geometry']]

    return gdf_centerline
