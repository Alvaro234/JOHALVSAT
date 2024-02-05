import rasterio
import matplotlib.pyplot as plt
import PIL as PIL
# Replace with the actual paths to your Sentinel-2 images
image_path = "data/combined_output/2024_combined.tif"
image_path1 = "data/cropped_combined/cropped_T29SQA_20240121T111259_B02_10m.jp2"
image_path2 = "data/cropped_combined/cropped_T29SQA_20240121T111259_B03_10m.jp2"
image_path3 = "data/cropped_combined/cropped_T29SQA_20240121T111259_B08_10m.jp2"



def display_image(ax, image_path, title):
    with rasterio.open(image_path) as src:
        ax.imshow(src.read(1))
        ax.set_title(title)
        ax.axis('off')
        
# Create a 2x2 subplot layout
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Display each image in a subplot
display_image(axs[0, 0], image_path, "Image 1")
display_image(axs[0, 1], image_path1, "Image 2")
display_image(axs[1, 0], image_path2, "Image 3")
display_image(axs[1, 1], image_path3, "Image 4")

plt.tight_layout()
plt.show()
