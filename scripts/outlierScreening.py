import numpy as np
import pymeshlab

# Define the path to your input PLY file
input_ply_file_path = r'C:\Users\conno\OneDrive\Documents\Capstone\miniproject-colmap\dense\fused.ply'

ms = pymeshlab.MeshSet()
ms.load_new_mesh(input_ply_file_path)
ms.save_current_mesh(input_ply_file_path, binary = False)

# Define user-specified bounds
x_min = -8  # Minimum X-coordinate
x_max = 10   # Maximum X-coordinate
y_min = -10  # Minimum Y-coordinate
y_max = 10   # Maximum Y-coordinate

# Define the path to the output PLY file
output_ply_file_path = "filtered_point_cloud.ply"

# Read the input PLY file and extract point cloud data
with open(input_ply_file_path, 'r') as f:
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
num_fields = 0
fields = []
for line in header_lines:
    if line.startswith("element vertex"):
        num_points = int(line.split()[-1])
    elif line.startswith("property"):
        num_fields += 1
        fields.append(line.strip())

# Extract point cloud data
point_cloud_data = np.zeros((num_points, num_fields), dtype=np.float32)
for i in range(num_points):
    values = list(map(float, data_lines[i].split()))
    point_cloud_data[i, :len(values)] = values

# Filter points based on user-specified bounds (X and Y only)
filtered_point_cloud = point_cloud_data[
    (point_cloud_data[:, 0] >= x_min) &
    (point_cloud_data[:, 0] <= x_max) &
    (point_cloud_data[:, 1] >= y_min) &
    (point_cloud_data[:, 1] <= y_max)
]

fields.insert(-1, "element face 0")

# Write the filtered point cloud to a new PLY file
with open(output_ply_file_path, 'w') as output_file:
    # Write the header
    output_file.write("ply\n")
    output_file.write("format ascii 1.0\n")
    output_file.write("comment VCGLIB generated\n")
    output_file.write("element vertex {}\n".format(len(filtered_point_cloud)))
    for field in fields:
        output_file.write(field + '\n')
    
    output_file.write("end_header\n")

    # Write the filtered point cloud data, handling unsigned char columns
    for point in filtered_point_cloud:
        output_file.write(" ".join(str(int(value)) if idx in [6, 7, 8, 9] else ("" if idx == 10 else str(value)) for idx, value in enumerate(point)) + '\n')

print(f"Filtered point cloud saved to {output_ply_file_path}")

