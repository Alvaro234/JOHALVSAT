#####################################################

# feed it to the ML algorithm that gives us a number (amount of vegetation?)
# Graph each of the number with its corresponding date so we can see the trend of how vegetation has declined in the long term?

#####################################################
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Define the directory where your satellite images are stored
image_dir = r'data'

# Create empty lists to store image data, years, months, and approximate NDVI values
image_data = []
years = []
months = []
ndvi_values = []

# Iterate through the image files in the directory
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        # Load the image
        image = Image.open(os.path.join(image_dir, filename))

        # Convert the image to a NumPy array
        image_array = np.array(image)

        # Extract the year and month by slicing the relevant part of the filename
        year_month = filename[:7]  # Extract the first 7 characters as the year and month
        year = year_month[:4]  # Extract the year part
        month = year_month[5:7]  # Extract the month part

        # Calculate approximate NDVI
        red_channel = image_array[:, :, 0]
        nir_channel = image_array[:, :, 2]

        # Normalize the channels to a 0-1 scale
        red_channel_normalized = red_channel / 255.0
        nir_channel_normalized = nir_channel / 255.0

        # Calculate approximate NDVI
        ndvi = (nir_channel_normalized - red_channel_normalized) / (nir_channel_normalized + red_channel_normalized)

        # Store the image data, year, month, and approximate NDVI
        image_data.append(image_array)
        years.append(year)
        months.append(month)
        ndvi_values.append(ndvi)

# Determine the number of images and calculate the subplot layout
num_images = len(image_data)
cols = 3  # Number of columns in the subplot (adjust as needed)
rows = (num_images + cols - 1) // cols  # Calculate the number of rows

# Create subplots procedurally based on the number of images
fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
for i, ax in enumerate(axs.flatten()):
    if i < num_images:
        ax.imshow(image_data[i])
        # Extract the approximate NDVI value from the center pixel
        ndvi_value = ndvi_values[i][image_array.shape[0] // 2, image_array.shape[1] // 2]
        ax.set_title(f'Date: {years[i]}-{months[i]}\nNDVI: {ndvi_value:.2f}')
        ax.axis('off')  # Hide axis labels

# Hide any empty subplots if the number of images is not a multiple of cols
for i in range(num_images, rows * cols):
    axs.flatten()[i].axis('off')

plt.tight_layout()
plt.show() #djgsodg
