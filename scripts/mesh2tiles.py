import pymeshlab
import shutil

def mesh2tiles(projdir):

    ms = pymeshlab.MeshSet()
    
    ms.load_new_mesh(projdir+r"\landscape.obj")

    fullmesh = ms.current_mesh_id()

    outdir = projdir + r"\out"

    _quad_slice(ms, fullmesh, projdir, outdir)

def _quad_slice(ms, fulltile, projdir, outdir):
    
    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect="(x < 0) || (y < 0)")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{1}.png")
    ms.set_texture_per_mesh( f"{outdir}\{fulltile}_{1}.png")

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect="(x < 0) || (y > 0)")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{2}.png")
    ms.set_texture_per_mesh( f"{outdir}\{fulltile}_{2}.png")

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect="(x > 0) || (y > 0)")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{3}.png")
    ms.set_texture_per_mesh( f"{outdir}\{fulltile}_{3}.png")

    ms.add_mesh(ms.mesh(fulltile))
    ms.compute_selection_by_condition_per_vertex(condselect="(x > 0) || (y < 0)")
    ms.meshing_remove_selected_vertices()
    shutil.copy(projdir + r"\landscape.png", f"{outdir}\{fulltile}_{4}.png")
    ms.set_texture_per_mesh( f"{outdir}\{fulltile}_{4}.png")

    for i in range(4):
        try:
            ms.set_current_mesh(i)
            ms.save_current_mesh(f"{outdir}\{fulltile}_{i}.obj")

        except:
            pass

mesh2tiles(r"C:\Users\akuhl\Downloads\testproj")