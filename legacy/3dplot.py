import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a grid of x and y values
x = np.linspace(-5, 5, 40)
y = np.linspace(-5, 5, 40)
x, y = np.meshgrid(x, y)

# Compute the z values using the given function
z = np.cos(np.sqrt(x**2 + y**2))

# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surface = ax.plot_surface(x, y, z, cmap='viridis')

# Add labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add a color bar
fig.colorbar(surface, shrink=0.5, aspect=5)

# Show the plot
plt.show()