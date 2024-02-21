from matplotlib import pyplot
from plyfile import PlyData, PlyElement
import pathlib as pl

def get_coordinates(filename):
    plydata = PlyData.read(filename)
    vertex = plydata['vertex']
    x = vertex['x']
    y = vertex['y']
    return x, y

def create_heat_map(file, outdir):
    filename = file
    x, y = get_coordinates(filename)
    pyplot.hexbin(x, y, gridsize=50, cmap='Blues', mincnt=1)
    pyplot.xlabel('X')
    pyplot.ylabel('Y')
    pyplot.title('Dense Point Cloud')
    pyplot.savefig(pl.Path(outdir / "heat_map.png"))
    pyplot.close('all')
    # TODO: Warning created when using Matplotlib outside of main thread, works for me but needs testing

def remove_points(file, minx, maxx, miny, maxy):
    plydata = PlyData.read(file)
    vertex = plydata['vertex']
    x = vertex['x']
    y = vertex['y']
    mask = (x >= minx) & (x <= maxx) & (y >= miny) & (y <= maxy)
    vertex = vertex[~mask]
    new_vertex = PlyElement.describe(vertex, 'vertex')
    new_plydata = PlyData([new_vertex], text=plydata.text)
    file = str(file)
    new_plydata.write(file)

#create_heat_map(pl.Path(r"C:\Users\akuhl\Downloads\test\dense\fused.ply"), pl.Path(r"C:\Users\akuhl\Downloads\test\dense"))
#remove_points(pl.Path(r"C:\Users\akuhl\Downloads\test\dense\fused.ply"), -10, 10, -10, 10)

# import numpy as np
# import matplotlib.pyplot as plt
# import pathlib as pl
# class PointCloudManager:
#     def __init__(self,path):
#         self.input_ply_file_path = path

#     def read_ply_file(self):
#         with open(self.input_ply_file_path, 'r') as f:
#             lines = f.readlines()

#         header_lines = []
#         data_lines = []

#         is_data = False
#         for line in lines:
#             if is_data:
#                 data_lines.append(line.strip())
#             elif line.strip().lower() == "end_header":
#                 is_data = True
#             else:
#                 header_lines.append(line.strip())

#         # Parse header information
#         num_points = 0
#         num_fields = 0
#         fields = []
#         for line in header_lines:
#             if line.startswith("element vertex"):
#                 num_points = int(line.split()[-1])
#             elif line.startswith("property"):
#                 num_fields += 1
#                 fields.append(line.strip())

#         # Extract point cloud data
#         point_cloud_data = np.zeros((num_points, num_fields), dtype=np.float32)
#         for i in range(num_points):
#             values = list(map(float, data_lines[i].split()))
#             point_cloud_data[i, :len(values)] = values

#         return point_cloud_data, fields

#     def filter_point_cloud(self, x_min, x_max, y_min, y_max):
#         point_cloud_data, fields = self.read_ply_file()

#         # Filter points based on user-specified bounds (X and Y only)
#         filtered_point_cloud = point_cloud_data[
#             (point_cloud_data[:, 0] >= x_min) &
#             (point_cloud_data[:, 0] <= x_max) &
#             (point_cloud_data[:, 1] >= y_min) &
#             (point_cloud_data[:, 1] <= y_max)
#             ]
#         with open(pl.Path(r"dense\filtered.ply"), 'w') as output_file:
#             # Write the header
#             output_file.write("ply\n")
#             output_file.write("format ascii 1.0\n")
#             output_file.write("comment VCGLIB generated\n")
#             output_file.write("element vertex {}\n".format(len(filtered_point_cloud)))
#             for field in fields:
#                 output_file.write(field + '\n')

#             output_file.write("end_header\n")

#             # Write the filtered point cloud data, handling unsigned char columns
#             for point in filtered_point_cloud:
#                 formatted_point = ["{:.7f}".format(value) if idx not in [3, 4, 5, 6] else str(int(value)) for idx, value in enumerate(point[:-1])]
#                 formatted_point.append(str(int(point[-1])))
#                 output_file.write(" ".join(formatted_point).rstrip('0').rstrip('.') + '\n')

#     def generate_image(self):
#         # Read the input PLY file and extract x and y coordinates
#         with open(self.input_ply_file_path, 'r') as f:
#             lines = f.readlines()

#         header_lines = []
#         data_lines = []

#         is_data = False
#         for line in lines:
#             if is_data:
#                 data_lines.append(line.strip())
#             elif line.strip().lower() == "end_header":
#                 is_data = True
#             else:
#                 header_lines.append(line.strip())

#         # Parse header information
#         num_points = 0
#         num_fields = 0
#         fields = []
#         for line in header_lines:
#             if line.startswith("element vertex"):
#                 num_points = int(line.split()[-1])
#             elif line.startswith("property"):
#                 num_fields += 1
#                 fields.append(line.strip())

#         # Extract x and y coordinates
#         x_values = []
#         y_values = []
#         for i in range(num_points):
#             values = list(map(float, data_lines[i].split()))
#             x_values.append(values[0])
#             y_values.append(values[1])

#         # Create a hexbin plot (density map)
#         plt.hexbin(x_values, y_values, gridsize=50, cmap='Blues', mincnt=1)

#         # Set plot labels and title
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         plt.title('Density Map of Points')

#         # Save the plot as a PNG file
#         #plt.savefig(pl.Path(r"dense\density_map.png"))
#         plt.savefig(r"C:\Users\akuhl\Downloads\test\dense\density_map.png")

#         # Show the plot (optional)
#         #plt.show()


#     # Called by recon manager after matcher call
