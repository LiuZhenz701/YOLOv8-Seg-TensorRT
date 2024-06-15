# Print name tag from the ontology file in two different ways
import pandas as pd

df = pd.read_csv('/home/ubuntu/Desktop/InstanceSegment/Rellis_3D_pylon_camera_node/ontology.csv')

name_col = df.iloc[:, -2]
index = 0

# Print for data.yaml
"""
for name in name_col:
    print("  " + str(index) + ": " + name)
    index += 1
"""

# Print for class-names(TensorRT)
for name in name_col:
    print(name, end=" ")
    index += 1