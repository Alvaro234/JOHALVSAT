import os
from PIL import Image
import numpy as np
import re
import matplotlib.pyplot as plt

# Define the directory where your satellite images are stored
image_dir = r'C:\Users\alvar\Desktop\Python\JOHALVSAT\data'

# Create empty lists to store image data and dates
image_data = []
dates = []

# Define a regular expression pattern to extract the date from the file name
date_pattern = r'\d{4}-\d{2}-\d{2}-\d{2}_\d{2}_\d{4}-\d{2}-\d{2}-\d{2}_\d{2}_\d{2}_Sentinel-2_L2A_True_color'

# Iterate through the image files in the directory
for filename in os.listdir(image_dir):
    if filename.endswith('.jpg'):
        # Load the image
        image = Image.open(os.path.join(image_dir, filename))
        
        # Convert the image to a NumPy array
        image_array = np.array(image)
        
        # Extract the date from the filename
        match = re.search(date_pattern, filename)
        if match:
            date = match.group()
        else:
            date = 'Unknown'  # Set a default if date not found
        
        # Store the image data and date
        image_data.append(image_array)
        dates.append(date)

# Now you have 'image_data' containing the image data and 'dates' containing the corresponding dates.

# Determine the number of images and calculate the subplot layout
num_images = len(image_data)
cols = 3  # Number of columns in the subplot (adjust as needed)
rows = (num_images + cols - 1) // cols  # Calculate the number of rows

# Create subplots procedurally based on the number of images
fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
for i, ax in enumerate(axs.flatten()):
    if i < num_images:
        ax.imshow(image_data[i])
        ax.set_title(f'Date: {dates[i]}')
        ax.axis('off')  # Hide axis labels

# Hide any empty subplots if the number of images is not a multiple of cols
for i in range(num_images, rows * cols):
    axs.flatten()[i].axis('off')

plt.tight_layout()
plt.show()

# feed it to the ML algorithm that gives us a number (amount of vegetation?)
# Graph each of the number with its corresponding date so we can see the trend of how vegetation has declined in the long term?
