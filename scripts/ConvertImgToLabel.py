# Run this file to convert all color label images from the Rellis-3D Github Repository
# to yolo required .txt format 
import pandas as pd
import cv2
import numpy as np
import os

# Get the color index from the ontology file
# Return the first column
def get_first_col(file_path):
    df = pd.read_csv(file_path)

    first_col = df.iloc[:, 0]

    return first_col

# Convert hexdecimal color index to RGB
# Return the RGB index of the input column
def hex_to_rgb(codes):
    rgb_codes = []
    for code in codes:
        code = code.lstrip('#')
        rgb = tuple(int(code[i : i+2], 16) for i in (0, 2, 4))
        rgb_codes.append(rgb)
    return rgb_codes

# Path to ontology file, replace the directory with the one on your workspace
ontology_path = '/home/ubuntu/Desktop/InstanceSegment/ontology.csv'

# Get the RGB index from the ontology file
color_col = get_first_col(ontology_path)
rgb_codes = hex_to_rgb(color_col)

# Label each color with index from 0 to 20
color_mapping = {rgb : idx for rgb, idx in zip(rgb_codes, range(20))}

# Convert color label image to binary image and change it to yolo format
"""
    color_image - the color label image
    output_dir - the desired directory for the yolo format .txt file
    image_name - the name of the color label image
    color_mapping - the color list with their index
"""
def convert_color_to_yolo_format(color_image, output_dir, image_name, color_mapping):
    
    color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

    for color, class_id in color_mapping.items():
        mask = np.all(color_image_rgb == color, axis=-1).astype(np.uint8) * 255

        H, W = mask.shape
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        polygons = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 200:
                polygon = []
                for point in cnt:
                    x, y = point[0]
                    polygon.append(x / W)
                    polygon.append(y / H)
                polygons.append(polygon)

        output_file = os.path.join(output_dir, os.path.splitext(image_name)[0] + '.txt')
        with open(output_file, 'a') as f:
            for polygon in polygons:
                f.write(f'{class_id} ')
                f.write(' '.join(map(str, polygon)))
                f.write('\n')

# Helper function to write the .txt file to the dedicated directory
"""
    image_dir - the folder of the color label images
    output_dir - the folder to store all the .txt labels of the input color label images
    color_mapping - the color list with their index
"""
def process_directory(image_dir, output_dir, color_mapping):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_name in os.listdir(image_dir):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, image_name)
            color_image = cv2.imread(image_path)
            convert_color_to_yolo_format(color_image, output_dir, image_name, color_mapping)

# Change the image_dir and output_dir with the correct path on your workspace
# (you can ignore the variable 'index' below)

# Note that you must do this folder by folder, follow the index from '00000' to '00004', or
# the method for deleting redundant files will not work
index = "00002"
image_dir = '/home/ubuntu/Desktop/InstanceSegment/Rellis_3D_pylon_camera_node/Color_Label/' + index + '/pylon_camera_node_label_color'
output_dir = '/home/ubuntu/Desktop/InstanceSegment/Rellis_3D_pylon_camera_node/Color_Label/' + index + '/label'

process_directory(image_dir, output_dir, color_mapping)