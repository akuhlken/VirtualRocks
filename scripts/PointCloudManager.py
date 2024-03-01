import os
import shutil
from matplotlib import pyplot
from plyfile import PlyData, PlyElement
import pathlib as pl
import warnings

warnings.filterwarnings("ignore")

def get_coordinates(filename):
    """
    Helper method which extract the x and y coordinates from the given `.ply` file.

    Args:
        filename (pathlib.Path): Path to a .ply point cloud file
    """
    plydata = PlyData.read(filename)
    vertex = plydata['vertex']
    x = vertex['x']
    y = vertex['y']
    return x, y

def create_heat_map(filename, outdir):
    """
    Creates a heat map of the dense point cloud and exports it as `heat_map.png` in the dense
    directory.

    Args:
        filename (pathlib.Path): Path to a .ply point cloud file
        outdir (pathlib.Path): Output directory
    """
    x, y = get_coordinates(filename)
    pyplot.hexbin(x, y, gridsize=50, cmap='Blues', mincnt=1)
    pyplot.xlabel('X')
    pyplot.ylabel('Y')
    pyplot.title('Dense Point Cloud')
    pyplot.savefig(pl.Path(str(outdir)) / "heat_map.png")
    pyplot.close('all')

def remove_points(filename, minx, maxx, miny, maxy):
    """
    Method removes points from .ply point cloud that lie outside the provided bounds and exports as
    ``fused.ply`` into the dense directory.

    Args:
        filename (pathlib.Path): Path to a .ply point cloud file
        minx (int): min x value
        maxx (int): max x value
        miny (int): min y value
        maxy (int): max y value
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