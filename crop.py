## This file is to crop the images downloaded from the sentinel 2.

from osgeo import ogr
from osgeo import gdal
from shapely.geometry import shape
from shapely.geometry import mapping
import geopandas as gpd
import os

def crop_image(input_image_path, output_image_path, aoi_kml_path):
    # Open KML/KMZ file
    kml_ds = ogr.Open(aoi_kml_path)
    kml_layer = kml_ds.GetLayer()

    # Extract geometry from KML
    feature = kml_layer.GetFeature(0)
    geom = feature.GetGeometryRef()

    # Convert KML geometry to Shapely geometry
    shp_geometry = shape(mapping(geom))

    # Open the Sentinel-2 image
    image_ds = gdal.Open(input_image_path)

    # Crop the image using the KML geometry
    cropped_ds = gdal.Translate(output_image_path, image_ds,
                                format='GTiff',
                                projWin=[shp_geometry.bounds[0], shp_geometry.bounds[3],
                                         shp_geometry.bounds[2], shp_geometry.bounds[1]])

    # Close datasets
    kml_ds = None
    image_ds = None
    cropped_ds = None

if __name__ == "__main__":
    # Replace these paths with your actual paths
    input_image_path = "path/to/your/Sentinel2_image.tif"
    output_image_path = "path/to/save/cropped/image.tif"
    aoi_kml_path = "path/to/your/area.kml"

    # Call the function to crop the image
    crop_image(input_image_path, output_image_path, aoi_kml_path)

    print(f"Image cropped successfully. Cropped image saved at {output_image_path}")
