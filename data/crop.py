import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
import matplotlib.pyplot as plt
#input_image_path = "2023_B04_20m.jp2"
#output_image_path = "cropped_2023_B04_20m.jp2"
#crop_geometry = {"type":"Polygon","coordinates":[[[-6.16516,36.989391],[-6.482608,36.989391],[-6.482608,36.791689],[-6.16516,36.791689],[-6.16516,36.989391]]]}

def crop_image(input_image_path, output_image_path, crop_geometry):
    with rasterio.open(input_image_path) as src:
        out_image, out_transform = mask(src, [crop_geometry], crop=True)
        out_meta = src.meta.copy()

    # Update the driver to GeoTIFF
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    # Save the cropped image as GeoTIFF
    with rasterio.open(output_image_path, "w", **out_meta) as dest:
        dest.write(out_image)

def display_image(image_path):
    with rasterio.open(image_path) as src:
        plt.imshow(src.read(1), cmap='viridis')
        plt.title("Cropped Image")
        #plt.colorbar()
        plt.show()

# Replace these paths with your actual paths
input_image_path = "data/raw/2024_B04_20m.jp2"
output_image_path = "cropped_2023_B8A_20m.jp2"

# Recognise boundary
with rasterio.open(input_image_path) as src:
    # Get the coordinates of the top-left and bottom-right corners
    top_left = (src.bounds.left, src.bounds.top)
    bottom_right = (src.bounds.right, src.bounds.bottom)
print("Top-left corner coordinates:", top_left)
print("Bottom-right corner coordinates:", bottom_right)

# Specify the bounds from the provided top-left and bottom-right corner coordinates
top_left_x, top_left_y = src.bounds.left, src.bounds.top
bottom_right_x, bottom_right_y = src.bounds.right, src.bounds.bottom

# Calculate the coordinates for the top half of the image (KEEP THIS PARAMETERS LIKE THIS AND DO NOT TOUCH THEM)
crop_minx, crop_miny = top_left_x*1.02, top_left_y
crop_maxx, crop_maxy = (top_left_x + bottom_right_x) /2.0099, (top_left_y + bottom_right_y) / 1.987

# Create a bounding box geometry
crop_geometry = box(crop_minx, crop_miny, crop_maxx, crop_maxy)

print(f"{crop_geometry}")

# Call the function to crop the image
crop_image(input_image_path, output_image_path, crop_geometry)

print(f"Image cropped successfully. Cropped image saved at {output_image_path}")

#display_image(output_image_path)