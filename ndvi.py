import os
import re
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def find_band_paths(cropped_folder, band_name):
    band_paths = []
    for filename in os.listdir(cropped_folder):
        if filename.endswith(".jp2") and band_name in filename:
            band_paths.append(os.path.join(cropped_folder, filename))
    return band_paths

def calculate_ndvi(band4_path, band8_path, output_ndvi_path):
    with rasterio.open(band4_path) as src4, rasterio.open(band8_path) as src8:
        # Read band data
        band4 = src4.read(1).astype(np.float32)
        band8 = src8.read(1).astype(np.float32)

        # Calculate NDVI
        ndvi = np.where(
            (band8 + band4) == 0,
            0,
            (band8 - band4) / (band8 + band4)
        )

        # Metadata from band 4
        ndvi_meta = src4.meta.copy()
        ndvi_meta.update({"driver": "GTiff", "count": 1, "dtype": "float32"})

        # Write NDVI to a new GeoTIFF file
        with rasterio.open(output_ndvi_path, "w", **ndvi_meta) as dst:
            dst.write(ndvi, 1)

def calculate_ndvi_for_all_years(cropped_folder, output_ndvi_folder, colormap='viridis', vmin=-1, vmax=1):
    for filename in os.listdir(cropped_folder):
        if filename.endswith("_B04_10m.jp2"):
            year = re.search(r'(\d{4})', filename).group(1)
            band4_path = os.path.join(cropped_folder, filename)
            band8_path = os.path.join(cropped_folder, filename.replace("B04", "B08"))

            # Output NDVI path for each scene
            output_ndvi_path = os.path.join(output_ndvi_folder, f"ndvi_{year}_{os.path.splitext(filename)[0]}.tif")

# Replace with the actual paths to your cropped band 4 and band 8 images
#band4_path = "data/cropped/cropped_2023_B04_20m.jp2"
#band8_path = "data/cropped/cropped_2023_B8A_20m.jp2"
#output_ndvi_path = "data/cropped/ndvi_image.tif"

#Johannes paths
band4_path = "JOHALVSAT/data/cropped/cropped_2023_B04_10m.jp2"
band8_path = "JOHALVSAT/data/cropped/cropped_2023_B08_10m.jp2"
output_ndvi_path = "JOHALVSAT/data/cropped/ndvi_image.tif"



            # Calculate and save NDVI, then display the NDVI image
            calculate_ndvi(band4_path, band8_path, output_ndvi_path)
            #display_ndvi(output_ndvi_path, colormap, vmin, vmax)
# Replace with the actual path to your output NDVI folder
output_ndvi_folder = "data/ndvi"

# Specify colormap and color range
colormap = 'viridis'
vmin = -1
vmax = 1

# Calculate and display NDVI for all years
cropped_folder = "data/cropped"
calculate_ndvi_for_all_years(cropped_folder, output_ndvi_folder, colormap, vmin, vmax)
