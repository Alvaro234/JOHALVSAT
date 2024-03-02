import json
import numpy as np
import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask
import cv2

#'JOHALVSAT/data/masks/crops.tif'
#'JOHALVSAT/data/masks/wetlands.tif'
#'JOHALVSAT/data/masks/dunes.tif'
#'JOHALVSAT/data/masks/pines.tif'

#'JOHALVSAT/data/ndvi/2021_ndvi.tif'
#'JOHALVSAT/data/ndvi/2022_ndvi.tif'
#'JOHALVSAT/data/ndvi/2023_ndvi.tif'
#'JOHALVSAT/data/ndvi/2024_ndvi.tif'


# Paths to directories
tif_directory = 'JOHALVSAT/data/ndvi'
mask_directory = 'JOHALVSAT/data/masks'

# List of masks to apply
mask_labels = ["crops", "dunes", "pines", "wetlands"]

# Initialize vector to store resulting images
result_images = []

# Iterate over TIFF images in the directory
for filename in os.listdir(tif_directory):
    if filename.endswith('.tif'):
        # Load TIFF image
        tif_path = os.path.join(tif_directory, filename)
        with rasterio.open(tif_path, 'r') as src:
            tif_image = src.read()

        # Get image dimensions
        image_height, image_width, _ = tif_image.shape
        
        # Initialize mask to store combined masks
        combined_mask = np.zeros((image_height, image_width), dtype=np.uint8)
        
        # Iterate over mask labels
        for label in mask_labels:
            # Load mask
            mask_filename = f"{label}.tif"
            mask_path = os.path.join(mask_directory, mask_filename)
            with rasterio.open(mask_path, 'r') as src:
                mask_image = src.read(1)
            
            # Generate mask for current label
            current_mask = generate_mask(label, image_height, image_width, mask_image)
            
            # Combine masks
            combined_mask = cv2.bitwise_or(combined_mask, current_mask)
        
        # Apply combined mask to TIFF image
        masked_image = cv2.bitwise_and(tif_image, tif_image, mask=combined_mask)
        
        # Append resulting image to vector
        result_images.append(masked_image)

# Convert list of images to numpy array
result_images = np.array(result_images)
