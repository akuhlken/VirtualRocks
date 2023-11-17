import pymeshlab
import shutil
import os

def mesh2tiles(projdir):

    ms = pymeshlab.MeshSet()
    
    ms.load_new_mesh(projdir+r"\landscape.obj")

    fullmesh = ms.current_mesh_id()

    outdir = projdir + r"\out"
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    _quad_slice(ms, fullmesh, projdir, outdir, 3)

def _quad_slice(ms, fulltile, projdir, outdir, depth):

    ms.set_current_mesh(fulltile)
    min=ms.current_mesh().bounding_box().min()
    max=ms.current_mesh().bounding_box().max()

    minx = min[0] 
    maxx = max[0]
    miny = min[1]
    maxy = max[1]

    midx = (maxx + minx) / 2
    midy = (maxy + miny) / 2

    tiles = []

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {midx}) || (y < {midy})")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{1}.png")
    ms.set_texture_per_mesh(textname= f"{outdir}\{fulltile}_{1}.png")
    tiles.append(ms.current_mesh_id())

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {midx}) || (y > {midy})")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{2}.png")
    ms.set_texture_per_mesh(textname= f"{outdir}\{fulltile}_{2}.png")
    tiles.append(ms.current_mesh_id())

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x > {midx}) || (y > {midy})")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{3}.png")
    ms.set_texture_per_mesh(textname= f"{outdir}\{fulltile}_{3}.png")
    tiles.append(ms.current_mesh_id())

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x > {midx}) || (y < {midy})")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{4}.png")
    ms.set_texture_per_mesh(textname= f"{outdir}\{fulltile}_{4}.png")
    tiles.append(ms.current_mesh_id())

    for tile in tiles:
        try:
            ms.set_current_mesh(tile)
            ms.save_current_mesh(f"{outdir}\{fulltile}_{tile}.obj")

        except:
            # This should not need to be here... but it errors for no reason
            # https://github.com/cnr-isti-vclab/PyMeshLab/issues/129
            pass

    depth -= 1
    if depth > 0:
        print(f"depth: {depth}")
        path = f"{projdir}\out\depth{depth}"
        if not os.path.exists(path):
            os.makedirs(path)
        _quad_slice(ms, tiles[0], projdir, path, depth)
        _quad_slice(ms, tiles[1], projdir, path, depth)
        _quad_slice(ms, tiles[2], projdir, path, depth)
        _quad_slice(ms, tiles[3], projdir, path, depth)

mesh2tiles(r"C:\Users\akuhl\Downloads\testproj")