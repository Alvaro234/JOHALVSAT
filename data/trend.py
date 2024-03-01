import json
import numpy as np
import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask
import cv2

#ndvi_image_file = 'JOHALVSAT/data/ndvi/2021_ndvi.tif'
#polygons_file = 'JOHALVSAT/data/polygons.json'



# Read LabelMe JSON file
with open('JOHALVSAT\data\polygons.json', 'r') as f:
    labelme_data = json.load(f)

# Get image dimensions
image_height = labelme_data['imageHeight']
image_width = labelme_data['imageWidth']


# Initialize mask
mask = np.zeros((image_height, image_width), dtype=np.uint8)

# Works until this point

# Iterate through annotations
for annotation in labelme_data['shapes']:
    # Extract polygon vertices
    polygon = np.array(annotation['points'], dtype=np.int32)
    polygon = polygon.reshape((-1, 2))

    # Create binary mask for polygon
    polygon_mask = np.zeros((image_height, image_width), dtype=np.uint8)
    cv2.fillPoly(polygon_mask, [polygon], 255)

    # Add polygon mask to the overall mask
    mask = cv2.bitwise_or(mask, polygon_mask)


# Save the mask as an image
cv2.imwrite('mask.png', mask)



"""
# Read JSON data
##JOHALVSAT\data\combined_output\polygons.json Relative path 
#with open('polygons.json', 'r') as f:
    #json_data = json.load(f)

# Load polygons from JSON file
polygons_file = 'JOHALVSAT\data\polygons.json'
polygons = gpd.read_file(polygons_file)

# Load NDVI image
#ndvi_image_file = 'path/to/your/ndvi_image.tif'
#with rasterio.open(ndvi_image_file) as src:
#    ndvi_image = src.read(1)  # Assuming NDVI is stored in the first band

image_dir = 'JOHALVSAT\data\ndvi'
for filename in os.listdir(image_dir):
    if filename.endswith('.tif'):
# Check the values inside the each polygon and compare them to other years

        for polygon in json_data['polygons']:
            print('Polygon Name:', polygon['name'])
        
        # Extract polygon coordinates
        points = polygon['points']
        num_points = len(points)
        polygon_x = [point['x'] for point in points]
        polygon_y = [point['y'] for point in points]
        
        # Check matrix values within polygon
        for x, y in zip(polygon_x, polygon_y):
            print('Value at ({}, {}): {:.4f}'.format(x, y, matrix_data[y, x]))

average_ndvi_values = []
for polygon in polygons.geometry:
    average_ndvi = calculate_average_ndvi(ndvi_image, polygon)
    average_ndvi_values.append(average_ndvi)

# Now you have a list of average NDVI values for each polygon
print("Average NDVI values for each polygon:", average_ndvi_values)
"""