import os
import matplotlib.pyplot as plt
import rasterio

# Replace 'folder_path' with the path to your folder containing TIFF images
folder_path = "data/ndvi/"

# Get a list of all TIFF files in the folder
tif_files = [file for file in os.listdir(folder_path) if file.endswith(".tif")]

# Create a figure with subplots
num_images = len(tif_files)
num_rows = 1
num_cols = num_images

fig, axes = plt.subplots(num_rows, num_cols, figsize=(4 * num_cols, 4))

# Loop through each TIFF file and display it in a subplot
for i, tif_file in enumerate(tif_files):
    tif_path = os.path.join(folder_path, tif_file)

    with rasterio.open(tif_path) as src:
        image_data = src.read(1)  # Assuming a single-band image
        cmap = 'gray'  # You can change the colormap as needed

    # Display the image in the subplot
    axes[i].imshow(image_data, cmap=cmap)
    axes[i].set_title(f"Image {i+1}")

# Add a common colorbar for all subplots
cbar = fig.colorbar(axes[0].imshow(image_data, cmap=cmap), ax=axes, orientation='vertical', fraction=0.02, pad=0.1)
cbar.set_label('Pixel Values')

# Adjust layout and show the figure
#plt.tight_layout()
plt.show()
