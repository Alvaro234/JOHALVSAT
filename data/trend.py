import json
import numpy as np




# Read JSON data
##JOHALVSAT\data\combined_output\polygons.json Relative path 
with open('polygons.json', 'r') as f:
    json_data = json.load(f)

with open()
# Check the values inside the each polygon and compare them to other years

for polygon in json_data['polygons']:
    print('Polygon Name:', polygon['name'])
    
    # Extract polygon coordinates
    points = polygon['points']
    num_points = len(points)
    polygon_x = [point['x'] for point in points]
    polygon_y = [point['y'] for point in points]
    
    # Check matrix values within polygon
    for x, y in zip(polygon_x, polygon_y):
        print('Value at ({}, {}): {:.4f}'.format(x, y, matrix_data[y, x]))