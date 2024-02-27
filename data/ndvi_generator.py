import matplotlib.pyplot as plt
import numpy as np
import rasterio

# Load the individual channel images (red, green, blue, yellow)
red_channel = rasterio.open('data\cropped_bands\cropped_2021_B04_10m.jp2').read(1)
green_channel = rasterio.open('data\cropped_bands\cropped_2021_B03_10m.jp2').read(1)
blue_channel = rasterio.open('data\cropped_bands\cropped_2021_B02_10m.jp2').read(1)
nir_channel = rasterio.open('data\cropped_bands\cropped_2021_B08_10m.jp2').read(1)

# Normalize each channel to [0, 255]
def normalize_channel(channel):
    min_val = channel.min()
    max_val = channel.max()
    normalized = (channel - min_val) / (max_val - min_val) * 255
    normalized = np.round(np.clip(normalized, 0, 255))

    return normalized.astype(np.uint8)  # Ensure data type is uint8


red_normalized = normalize_channel(red_channel)
green_normalized = normalize_channel(green_channel)
blue_normalized = normalize_channel(blue_channel)

# Combine the channels to form the RGB image
rgb_image = np.dstack((red_normalized, green_normalized, blue_normalized))

# Apply gamma correction
gamma = 0.8
gamma_corrected_image = np.clip(rgb_image ** (1/gamma), 0, 255).astype(np.uint8)

print(rgb_image[100,100,1])
print(gamma_corrected_image[100,100,1])

# Display the image
plt.imshow(gamma_corrected_image)
plt.axis('off')  # Hide axes
plt.title('Combined RGB Image')
plt.show()

def ndvi_calc(band4,band8):
    # Calculate NDVI
    ndvi = np.where(
        (band8/10000 + band4/10000) == 0,
        0,
        (band8/10000 - band4/10000) / (band8/10000 + band4/10000)
    )

    
    return ndvi

print(red_channel[100,100])
print(nir_channel[100,100])
print((ndvi_calc(red_channel,nir_channel))[100,100])


plt.imshow(ndvi_calc(red_channel,nir_channel),cmap='RdYlGn', vmin=-1, vmax=1)
plt.axis('off')  # Hide axes
plt.title('Combined RGB Image')
plt.show()