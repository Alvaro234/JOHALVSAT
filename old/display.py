import rasterio
import numpy as np
import matplotlib.pyplot as plt

def display_rgb_image(image_path):
    # Display the RGB image
        
        plt.imshow(plt.imread(image_path))
        plt.title("Combined RGB Image")
        plt.axis('off')  # Turn off axis
        plt.show()
    

        


display_rgb_image("data/combined_output/2021_combined.png")