from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the true-color Sentinel-2 image
image = Image.open(r'C:\Users\alvar\Desktop\Python\JOHALVSAT\data\2023-03-02-00_00_2023-03-02-23_59_Sentinel-2_L2A_True_color.jpg')

# Make it read all the images
# feed it to the ML algorithm that gives us a number (amount of vegetation?)
# Graph each of the number with its corresponding date so we can see the trend of how vegetation has declined in the long term?



# Convert the image to a NumPy array
image_array = np.array(image)

# Extract the red, green, and NIR (near-infrared) bands
red_band = image_array[:, :, 0]
green_band = image_array[:, :, 1]
nir_band = image_array[:, :, 2]

# Visualize NDVI (you may need to adjust the colormap for visualization)


plt.imshow(green_band, cmap='viridis')
plt.colorbar()
plt.title('NDVI Image')
plt.show()

# You can further analyze NDVI values to estimate vegetation cover.
