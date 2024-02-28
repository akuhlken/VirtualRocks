import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from plyfile import PlyData, PlyElement
import pathlib as pl
import warnings

warnings.filterwarnings("ignore")

# Extract the x,y coordiantes from the .ply file at filename
def get_coordinates(filename):
    """
        description

        Args:
            filename (type?): what is it? (str or path?)
        """
    plydata = PlyData.read(filename)
    vertex = plydata['vertex']
    x = vertex['x']
    y = vertex['y']
    z = vertex['z']
    return x, y, z

# Create a heat map of the point cloud at filename
#   Save as heat_map.png in the dense directory
def create_heat_map(filename, outdir):
    """
        description

        Args:
            filename (type?): what is it?
            outdir (type?): what is it?
        """
    x, y, z = get_coordinates(filename)
    min_val = min(np.min(x), np.min(y))
    max_val = max(np.max(x), np.max(y))
    plt.hexbin(x, y, gridsize=50, cmap='Blues', mincnt=1)
    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)
    plt.title('Dense Point Cloud')
    plt.savefig(pl.Path(str(outdir)) / "heat_map.png")
    plt.close('all')

def create_height_map(filename, outdir):
    """
    description

    Args:
        filename (type?): what is it?
        outdir (type?): what is it?
    """
    x, y, z = get_coordinates(filename)
    min_val = min(np.min(x), np.min(y))
    max_val = max(np.max(x), np.max(y))
    plt.hexbin(x, y, C=z, gridsize=50, cmap='viridis', mincnt=1)
    plt.colorbar(label='Height')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Dense Point Cloud')
    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)
    plt.savefig(pl.Path(str(outdir)) / "height_map.png")
    plt.close('all')

# Remove all points from point cloud at filename which are outside bounds
#   Save as fused.ply in the dense dir
def remove_points(filename, minx, maxx, miny, maxy):
    """
        description

        Args:
            filename (type?): what is it?
            maxx (int): what is it?
            minx (int): what is it?
            maxy (int): what is it?
            miny (int): what is it?
        """
    tempfile = pl.Path(filename).parent / "temp.ply"
    if os.path.isfile(tempfile):
        os.remove(tempfile)
    shutil.copy(filename, tempfile)
    plydata = PlyData.read(tempfile)
    vertex = plydata['vertex']
    x = vertex['x']
    y = vertex['y']
    mask = (x >= minx) & (x <= maxx) & (y >= miny) & (y <= maxy)
    vertex = vertex[mask]
    new_vertex = PlyElement.describe(vertex, 'vertex')
    new_plydata = PlyData([new_vertex], text=plydata.text)
    new_plydata.write(filename)