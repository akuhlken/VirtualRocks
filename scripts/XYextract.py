# Define the path to your input PLY file
input_ply_file_path = r'C:\Users\conno\OneDrive\Documents\Capstone\miniproject-colmap\dense\fusedLab.ply'
output_file_path = "XYcords.ply"

# Read the input PLY file and extract x and y coordinates
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

# Extract x and y coordinates
x_coords = []
y_coords = []
for i in range(num_points):
    values = list(map(float, data_lines[i].split()))
    x_coords.append(values[0])  # Assuming x-coordinate is the first field
    y_coords.append(values[1])  # Assuming y-coordinate is the second field

# Write x and y coordinates to a new file
with open(output_file_path, 'w') as output_file:
    for x, y in zip(x_coords, y_coords):
        output_file.write(f"X: {x}, Y: {y}\n")

print(f"X and Y coordinates saved to {output_file_path}")