#!/bin/bash

# Please change the path with your dedicated location
MODEL_PATH="/home/ubuntu/Desktop/InstanceSegment/runs/segment/train/weights/best.onnx"
IMAGE_FOLDER="/home/ubuntu/Desktop/InstanceSegment/TensorRT_Test/"
CLASS_NAMES="void dirt grass tree pole water sky vehicle object asphalt building log person fence bush concrete barrier uphill downhill puddle mud rubble"

# Iterate over each image in the folder
for IMAGE_PATH in "$IMAGE_FOLDER"/*.{jpg,png}; do
    if [ -f "$IMAGE_PATH" ]; then
        ./detect_object_image --model "$MODEL_PATH" --input "$IMAGE_PATH" --class-names $CLASS_NAMES

        if [ $? -ne 0 ]; then
            echo "Error processing $IMAGE_PATH"
            exit 1
        else
            echo "Successfully processed $IMAGE_PATH"
        fi
    fi
done

echo "Processing completed."
