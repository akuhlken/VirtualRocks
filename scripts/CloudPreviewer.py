import sys
import open3d

def show(filename):
    cloud = open3d.io.read_point_cloud(filename)
    open3d.visualization.draw_geometries([cloud])

# Get args from caller (Main) and start open3d preview
file = sys.argv[1]
try:
    show(file)
except Exception as e:
    print(e, flush=True)