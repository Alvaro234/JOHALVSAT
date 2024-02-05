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

def calculate_ndvi(band4_path, band8_path, output_ndvi_path, colormap='viridis', vmin=-1, vmax=1):
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

    # Display the NDVI image
    #display_ndvi(output_ndvi_path, colormap, vmin, vmax)

def calculate_ndvi_for_year(cropped_folder, year, output_ndvi_folder, colormap='viridis', vmin=-1, vmax=1):
    # Find band 4 and band 8 paths for the specified year
    band4_paths = find_band_paths(cropped_folder, f"{year}_B04_10m")
    band8_paths = find_band_paths(cropped_folder, f"{year}_B08_10m")

    for band4_path, band8_path in zip(band4_paths, band8_paths):
        # Extract the scene ID from the filenames
        match = re.search(r'(\d+)', os.path.basename(band4_path))
        scene_id = match.group(1) if match else "unknown"

        # Output NDVI path for each scene
        output_ndvi_path = os.path.join(output_ndvi_folder, f"ndvi_{year}_{scene_id}.tif")

        # Calculate and save NDVI, then display the NDVI image
        calculate_ndvi(band4_path, band8_path, output_ndvi_path, colormap=colormap, vmin=vmin, vmax=vmax)

def display_ndvi(ndvi_path, colormap, vmin, vmax):
    with rasterio.open(ndvi_path) as src:
        plt.imshow(src.read(1), cmap=colormap, vmin=vmin, vmax=vmax)
        plt.title("NDVI Image")
        plt.colorbar()
        plt.show()

# Replace with the actual path to your output NDVI folder
output_ndvi_folder = "data/ndvi"

# Specify the available years for 10m data
years_to_process = ["2021","2022","2023", "2024"]  # Add more years as needed

# Iterate through all years and calculate NDVI
for year_to_process in years_to_process:
    cropped_folder = os.path.join("data/cropped/", year_to_process)
    calculate_ndvi_for_year(cropped_folder, year_to_process, output_ndvi_folder, colormap='viridis', vmin=-1, vmax=1)
