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
        plt.colorbar()
        plt.show()

# Replace these paths with your actual paths
input_image_path = "C:/Users/alvar/OneDrive - Universidad Politécnica de Madrid/Desktop/Python/JOHALVSAT/data/raw/2024_B04_20m.jp2"
output_image_path = "cropped_2023_B04_20m.jp2"

# Replace these coordinates with your desired cropping specifications
crop_minx, crop_miny, crop_maxx, crop_maxy = (699960.0, 4100040.0, 809760.0, 3990240.0) 

# Create a bounding box geometry
crop_geometry = box(crop_minx, crop_miny, crop_maxx, crop_maxy)

# Call the function to crop the image
crop_image(input_image_path, output_image_path, crop_geometry)

print(f"Image cropped successfully. Cropped image saved at {output_image_path}")

display_image(output_image_path)