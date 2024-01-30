import os
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import matplotlib.pyplot as plt
import numpy as np
import cv2

image_dir = "JOHALVSAT/data/cropped"
#image_path = "JOHALVSAT/data/cropped/cropped_2021_B04_10m.jp2"
image_path = "JOHALVSAT/data/cropped/cropped_2021_B08_10m.jp2"
#image_path2 = "data/cropped/cropped_2023_B08_10m.jp2"
#image_path3 = "data/cropped/cropped_2024_B08_10m.jp2"

for filename in os.listdir(image_dir):
    if filename.endswith('B04_10m.jp2'):

    else

# Load the image
image = cv2.imread(image_path)

# Define the region of interest (ROI) coordinates
# Here, we define a rectangle region from (x1, y1) to (x2, y2)
x1, y1 = 50, 450  # Top-left corner of the rectangle
x2, y2 = 450, 850  # Bottom-right corner of the rectangle

# Extract the region of interest
roi = image[y1:y2, x1:x2]
# Calculate the average brightness of the ROI
average_brightness = np.mean(roi)

# Draw a rectangle around the ROI on the original image
roi_color = (0, 255, 0)  # Green color
thickness = 2
cv2.rectangle(image, (x1, y1), (x2, y2), roi_color, thickness)



# Annotate the image with the average brightness value
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image, f'Average brightness: {average_brightness:.3f}', (x1, y1 - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

# Display the image
cv2.imshow('Image with ROI and Average Brightness', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


print("Average brightness:", average_brightness)
