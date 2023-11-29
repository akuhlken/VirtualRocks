import shutil
import pymeshlab
import os
import sys

# Default Parameters
OVERLAP = 0.1 # Overlap ammount between tiles
TEXTURE_RES = 1024
CELL_SIZE = 0.0001 # Clustering decimation cell size
TILE_SIZE = 50000 # Will subdivide tiles until they are below this number of verts

def dense2mesh(projdir):
    # Path to Colmap dense folder
    base_path = projdir + r"\dense"

    # Create a new MeshSet object
    print("Loading pymeshlab")
    ms = pymeshlab.MeshSet()
    
    # Open Colmap project from sparse as well as dense recon (fused.ply)
    print("Importing project files")
    ms.load_project([base_path+r"\images\project.bundle.out", base_path+r'\images\project.list.txt'])
    
    # Import the fused.ply mesh
    print("Loading dense point cloud")
    ms.load_new_mesh(base_path+r"\fused.ply")

    # Point cloud simplification
    print("Optimizing Point Cloud")
    ms.meshing_decimation_clustering(threshold = pymeshlab.AbsoluteValue(CELL_SIZE))
    
    # Mesher
    print("Starting Poisson Mesher")
    ms.generate_surface_reconstruction_screened_poisson(depth = 12, samplespernode = 20, pointweight = 4)

    # TODO: If model is empty try again with lower depth values until it works
    
    # Wipe verticies colors
    print("Setting vertex colors")
    ms.set_color_per_vertex(color1 = pymeshlab.Color(255, 255, 255))

    outdir = projdir + r"\out"
    if os.path.exists(outdir):
       shutil.rmtree(outdir)
    os.makedirs(outdir)

    fullmodel = ms.current_mesh_id()
    _quad_slice(ms, fullmodel, outdir)

    ms.set_current_mesh(fullmodel)
    
    #Mesh simplification
    print("Creating low poly mesh")
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum = 100000, preserveboundary = True, preservenormal = True)

    # Remove non-manifold edges
    print("Removing non-manifold edges")
    ms.meshing_repair_non_manifold_edges()

    print("Building texture for low poly mesh")
    ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = "100k.jpg", usedistanceweight=False)
    # Export mesh
    print(fr"Exporting mesh to {outdir}\100k.obj")
    ms.save_current_mesh(fr"{outdir}\100k.obj")
    print("Done!")
    return True
    
def _quad_slice(ms, tilein, outdir):
    ms.set_current_mesh(tilein)

    if(ms.current_mesh().vertex_number() < TILE_SIZE):
        ms.set_current_mesh(tilein)
        # Build texture
        print(f"Building texture for land_{tilein}.obj")
        ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = f"land_{tilein}.jpg", usedistanceweight=False)
        # Export mesh
        print(fr"Exporting mesh to {outdir}\land_{tilein}.obj")
        ms.save_current_mesh(fr"{outdir}\land_{tilein}.obj")
        print()
        return

    min=ms.current_mesh().bounding_box().min()
    max=ms.current_mesh().bounding_box().max()

    minx = min[0] 
    maxx = max[0]
    miny = min[1]
    maxy = max[1]

    midx = (maxx + minx) / 2
    midy = (maxy + miny) / 2

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {midx-OVERLAP}) || (y < {midy-OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir)

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {midx-OVERLAP}) || (y > {midy+OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir)

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x > {midx+OVERLAP}) || (y > {midy+OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir)

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x > {midx+OVERLAP}) || (y < {midy-OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir)

#projdir = sys.argv[1]
dense2mesh(r"C:\Users\akuhl\Downloads\alltest")

#Algorithm for slicing:

# Call _quadslice with full mesh, max and min x and y
# select in bounds
# check num of verts in selection:

# if num verts < TIME_SIZE copy full mesh and cut (giving overlap)

# else make four recursive calls with new bounds but dont do any cutting ot copying
