import os
import shutil
from matplotlib import pyplot
from plyfile import PlyData, PlyElement
import pathlib as pl

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
    return x, y

# Create a heat map of the point cloud at filename
#   Save as heat_map.png in the dense directory
def create_heat_map(filename, outdir):
    """
        description

        Args:
            filename (type?): what is it?
            outdir (type?): what is it?
        """
    x, y = get_coordinates(filename)
    pyplot.hexbin(x, y, gridsize=50, cmap='Blues', mincnt=1)
    pyplot.xlabel('X')
    pyplot.ylabel('Y')
    pyplot.title('Dense Point Cloud')
    pyplot.savefig(pl.Path(str(outdir)) / "heat_map.png")
    pyplot.close('all')
    # TODO: Warning created when using Matplotlib outside of main thread, works for me but needs testing
    # Can warning be supressed if we're sure it works??

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
    # TODO: Remove temp.ply as end if possible