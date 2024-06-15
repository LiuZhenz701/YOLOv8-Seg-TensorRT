# This code is for delete the redundant file in the original image folder, since
# the amount of color label images is less than the original images
import os

# Change the folder_path_label and folder_path_image with the correct path on your workspace
# (you can ignore the variable 'index' below)

# Note that you must do this folder by folder, follow the index from '00000' to '00004', or
# the method will not work
index = "00002"
folder_path_label = '/home/ubuntu/Desktop/InstanceSegment/Rellis_3D_pylon_camera_node/Color_Label/' + index + '/label'
folder_path_image = '/home/ubuntu/Desktop/InstanceSegment/Rellis_3D_pylon_camera_node/Original_Image/Rellis-3D/' + index + '/pylon_camera_node/'

file_names_label = os.listdir(folder_path_label)
file_names_image = os.listdir(folder_path_image)

file_names_image.sort()
file_names_label.sort()

cur_file = 0


for idx, file_name in enumerate(file_names_label):
    name = file_name[:11]
    image_file_name = file_names_image[idx]
    if name != image_file_name[:11]:
        file_path = folder_path_label + '/' + file_name
        print(file_path)
    

