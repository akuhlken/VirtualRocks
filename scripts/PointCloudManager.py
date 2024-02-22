import os
import shutil
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
    x, y = get_coordinates(file)
    pyplot.hexbin(x, y, gridsize=50, cmap='Blues', mincnt=1)
    pyplot.xlabel('X')
    pyplot.ylabel('Y')
    pyplot.title('Dense Point Cloud')
    pyplot.savefig(pl.Path(str(outdir)) / "heat_map.png")
    pyplot.close('all')
    # TODO: Warning created when using Matplotlib outside of main thread, works for me but needs testing
    # Can warning be supressed if we're sure it works??

def remove_points(file, minx, maxx, miny, maxy):
    tempfile = pl.Path(file).parent / "temp.ply"
    if os.path.isfile(tempfile):
        os.remove(tempfile)
    shutil.copy(file, tempfile)
    plydata = PlyData.read(tempfile)
    vertex = plydata['vertex']
    x = vertex['x']
    y = vertex['y']
    mask = (x >= minx) & (x <= maxx) & (y >= miny) & (y <= maxy)
    vertex = vertex[mask]
    new_vertex = PlyElement.describe(vertex, 'vertex')
    new_plydata = PlyData([new_vertex], text=plydata.text)
    new_plydata.write(file)