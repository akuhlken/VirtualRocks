import pymeshlab
import os

# Desault Parameters
DEPTH = 3 # will produce 4^DEPTH number of tiles
OVERLAP = 0.5 # Overlap ammount between tiles
TEXTURE_RES = 1024
CELL_SIZE = 0.001 # Clustering decimation cell size

def dense2mesh(projdir):
    print("Loaded dense2mesh.py")
    flag = False
    # Path to Colmap dense folder
    base_path = projdir + r"\dense"

    # Create a new MeshSet object
    print("Loading pymeshlab")
    ms = pymeshlab.MeshSet()
    
    
    # Open Colmap project from sparse as well as dense recon (fused.ply)
    print("Importing project files")
    ms.load_project([base_path+r"\images\project.bundle.out", base_path+r'\images\project.list.txt'])
    
    
    # Import the fused.ply mesh
    print("Loading desne point cloud")
    ms.load_new_mesh(base_path+r"\fused.ply")


    # Point cloud simplification
    print("Optimizing Point Cloud")
    ms.meshing_decimation_clustering(threshold = pymeshlab.AbsoluteValue(CELL_SIZE))
    

    # Mesher
    print("Starting Poisson Mesher")
    ms.generate_surface_reconstruction_screened_poisson(depth = 8, samplespernode = 20, pointweight = 4)
    

    # Wipe verticies colors
    print("Setting vertex colors")
    ms.set_color_per_vertex(color1 = pymeshlab.Color(255, 255, 255))

    outdir = projdir + r"\out"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    fullmodel = ms.current_mesh_id()
    _quad_slice(ms, fullmodel, outdir, DEPTH)

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
    print(f"Exporting mesh to {outdir}/100k.obj")
    ms.save_current_mesh(f"{outdir}/100k.obj")
    print("Done!")
    return True
    

def _quad_slice(ms, tilein, outdir, depth):
    print("Slicing depth:", depth)

    if(depth==0):
        ms.set_current_mesh(tilein)
        # Build texture
        print(f"Building texture for land_{tilein}.obj")
        ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = f"land_{tilein}.jpg", usedistanceweight=False)
        # Export mesh
        print(f"Exporting mesh to {outdir}/land_{tilein}.obj")
        ms.save_current_mesh(f"{outdir}\land_{tilein}.obj")
        print()
        return

    ms.set_current_mesh(tilein)
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
    _quad_slice(ms, ms.current_mesh_id(), outdir, depth-1)

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {midx-OVERLAP}) || (y > {midy+OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir, depth-1)

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x > {midx+OVERLAP}) || (y > {midy+OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir, depth-1)

    ms.add_mesh(ms.mesh(tilein))
    ms.compute_selection_by_condition_per_vertex(condselect=f"(x > {midx+OVERLAP}) || (y < {midy-OVERLAP})")
    ms.meshing_remove_selected_vertices()
    _quad_slice(ms, ms.current_mesh_id(), outdir, depth-1)

#dense2mesh(r"C:\Users\akuhl\Downloads\testproj")