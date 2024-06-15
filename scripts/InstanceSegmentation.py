# Main file. Make sure all images and tags are working fine, run this file
# to train the model and get result

# Weights of the result can be checked in runs/segment/train/weight/best.pt
from ultralytics import YOLO

model = YOLO('best.pt')
results = model.train(data='/home/ubuntu/Desktop/InstanceSegment/YOLOV8IS/data.yaml', epochs = 40, imgsz = 640)