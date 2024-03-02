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

def crop_images_in_folder(input_folder, output_folder, crop_geometry):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    # Loop through all files and subfolders in the input folder
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith("_10m.jp2"):
                input_image_path = os.path.join(root, filename)
                relative_path = os.path.relpath(input_image_path, input_folder)
                output_image_path = os.path.join(output_folder, f"cropped_{filename}")

                crop_image(input_image_path, output_image_path, crop_geometry)
                print(f"Image cropped successfully: {output_image_path}")


# Recognise boundary
with rasterio.open("data/raw/2021/T29SQA_20210116T111319_B02_10m.jp2") as src:
    # Get the coordinates of the top-left and bottom-right corners
    top_left = (src.bounds.left, src.bounds.top)
    bottom_right = (src.bounds.right, src.bounds.bottom)
print("Top-left corner coordinates:", top_left)
print("Bottom-right corner coordinates:", bottom_right)

# Specify the bounds from the provided top-left and bottom-right corner coordinates
top_left_x, top_left_y = src.bounds.left, src.bounds.top
bottom_right_x, bottom_right_y = src.bounds.right, src.bounds.bottom
# Calculate the coordinates for the top half of the image
crop_minx, crop_miny = top_left_x*1.02, top_left_y
crop_maxx, crop_maxy = (top_left_x + bottom_right_x) /2.0000, (top_left_y + bottom_right_y) / 1.987

# Create a bounding box geometry
crop_geometry = box(crop_minx, crop_miny, crop_maxx, crop_maxy)
print(crop_geometry)

# Call the function to crop all images in the folder
input_folder = "data/raw"
output_folder = "data/cropped_combined"
crop_images_in_folder(input_folder, output_folder, crop_geometry)

