import rasterio
import numpy as np
import matplotlib.pyplot as plt



# DISCLAIMER: WE HAVE TO SWITCH TO 10M DATA SINCE THE B8 WE ARE USING IS B8A WHICH IS NOT THE SAME AS B8



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

def display_ndvi(ndvi_path):
    with rasterio.open(ndvi_path) as src:
        plt.imshow(src.read(1), cmap='viridis', vmin=-1, vmax=1)  # Diverging colormap for NDVI
        plt.title("NDVI Image")
        plt.colorbar()
        plt.show()

# Replace with the actual paths to your cropped band 4 and band 8 images
band4_path = "data/cropped/cropped_2023_B04_20m.jp2"
band8_path = "data/cropped/cropped_2023_B8A_20m.jp2"
output_ndvi_path = "data/cropped/ndvi_image.tif"

# Calculate and save NDVI
calculate_ndvi(band4_path, band8_path, output_ndvi_path)

# Display the NDVI image
display_ndvi(output_ndvi_path)
