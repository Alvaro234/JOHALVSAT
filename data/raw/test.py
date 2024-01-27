import rasterio

# Replace with the actual path to your Sentinel-2 image
image_path = "C:/Users/alvar/OneDrive - Universidad Politécnica de Madrid/Desktop/Python/JOHALVSAT/data/raw/2023_B04_20m.jp2"

with rasterio.open(image_path) as src:
    # Get the coordinates of the top-left and bottom-right corners
    top_left = (src.bounds.left, src.bounds.top)
    bottom_right = (src.bounds.right, src.bounds.bottom)

print("Top-left corner coordinates:", top_left)
print("Bottom-right corner coordinates:", bottom_right)