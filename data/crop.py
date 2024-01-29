import os
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import matplotlib.pyplot as plt

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
        plt.show()

def crop_images_in_folder(input_folder, output_folder, crop_geometry):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jp2"):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, f"cropped_{filename}")

            crop_image(input_image_path, output_image_path, crop_geometry)
            print(f"Image cropped successfully: {output_image_path}")

# Replace these paths with your actual paths
input_folder = "data/raw"  # Replace with the path to your folder containing images
output_folder = "data/cropped"  # Replace with the path to the output folder

# Recognise boundary
with rasterio.open("data/raw/2021_B04_10m.jp2") as src:
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

# Call the function to crop all images in the folder
crop_images_in_folder(input_folder, output_folder, crop_geometry)