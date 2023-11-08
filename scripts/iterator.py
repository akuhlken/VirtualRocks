import numpy as np

# Define the path to your PLY file
ply_file_path = r"your_path"

with open(ply_file_path, 'r') as f:
    lines = f.readlines()

header_lines = []
data_lines = []

is_data = False
for line in lines:
    if is_data:
        data_lines.append(line.strip())
    elif line.strip().lower() == "end_header":
        is_data = True
    else:
        header_lines.append(line.strip())

# Parse header information
num_points = 0
for line in header_lines:
    if line.startswith("element vertex"):
        num_points = int(line.split()[-1])
        break

# Extract point cloud data
point_cloud_data = np.zeros((num_points, 3), dtype=np.float32)
for i in range(num_points):
    values = list(map(float, data_lines[i].split()))
    point_cloud_data[i, :] = values[:3]

# Iterate through the point cloud data
for i, point in enumerate(point_cloud_data):
    x, y, z = point
    print(f"Point {i + 1}: x = {x}, y = {y}, z = {z}")