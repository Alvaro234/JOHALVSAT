import numpy as np
import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask
import cv2
import matplotlib.pyplot as plt
import json

# Load masks
masks_dir = 'data/masks/'
mask_files = [f for f in os.listdir(masks_dir) if f.endswith('.tif')]

# Loop through NDVI images
ndvi_dir = 'data/ndvi/'
ndvi_files = [f for f in os.listdir(ndvi_dir) if f.endswith('.tif')]

i=0
avg_array = np.zeros((len(ndvi_files)*len(mask_files),2))

for ndvi_file in ndvi_files:
    ndvi_path = os.path.join(ndvi_dir, ndvi_file)
    
    ndvi_image = rasterio.open(ndvi_path).read(1)
    
    for mask_file in mask_files:
    
        mask_path = os.path.join(masks_dir, mask_file)
        
        crops_mask = rasterio.open(mask_path).read(1) / 255

        crops_mask = np.ma.masked_equal(crops_mask, np.nan)
        plt.imshow(crops_mask)
        masked_image = ndvi_image*crops_mask
        
        
        # Mask generation
        #masked_image = crops_mask * ndvi_image
        ############################## Save #####################

        # Define output file path
        output_file = os.path.join('data/output', f"{ndvi_file[:-4]}_{mask_file[:-4]}.tif")
        # Define metadata
        metadata = {
            'driver': 'GTiff',
            'dtype': 'float32',  # Adjust data type as needed
            'count': 1,  # Number of bands
            'height': masked_image.shape[0],  # Height of the array
            'width': masked_image.shape[1],  # Width of the array
        }
        # Write to a new TIFF file
        with rasterio.open(output_file, 'w', **metadata) as dst:
            dst.write(masked_image, 1)  # Assuming NDVI is stored in the first band

        print(f"Masked NDVI image saved to {output_file}")
        # Display the image
        plt.imshow(masked_image)
        plt.axis('off')  # Hide axes
        plt.title(f'NDVI masked with {mask_file}')
        plt.show()

        ############################## Save ######################
        masked_image = np.ma.masked_less_equal(masked_image, 0)
        avg = np.mean(masked_image)
        print(f"Average NDVI with mask {mask_file}: {avg}")
        
        avg_array[i,0] = i
        avg_array[i,1] = avg
        i = i+1


