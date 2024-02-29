import pymeshlab

def _load_point_cloud(file):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file)
    return ms

def show(file):
    ms = _load_point_cloud(file)
    ms.show_polyscope()