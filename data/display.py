import rasterio
import numpy as np
import matplotlib.pyplot as plt

def display_rgb_image(image_path):
    with rasterio.open(image_path) as src:
        # Read the RGB image data
        rgb_image = src.read()

        # Transpose the shape to (channels, height, width)
        rgb_image = np.transpose(rgb_image, (1, 2, 0))

        # Ensure the data type is float
        rgb_image = rgb_image.astype(np.float32)

        # Normalize the image to [0, 1] range
        rgb_image = rgb_image / 65535.0

        # Ensure the color channels are in the correct order (RGB)
        rgb_image = rgb_image[:, :, [2, 1, 0]]

        # Display the RGB image
        plt.imshow(rgb_image)
        plt.title("Combined RGB Image")
        plt.axis('off')  # Turn off axis
        plt.show()


display_rgb_image("data/combined_output/2021_combined_rgb.tif")