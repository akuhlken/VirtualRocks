import pymeshlab

flag = False

def dense2mesh(projdir):
    print("Loaded dense2mesh.py")
    flag = False
    # Path to Colmap dense folder
    base_path = projdir + r"\dense"

    # Create a new MeshSet object
    print("Loading pymeshlab")
    ms = pymeshlab.MeshSet()
    if flag: 
        ~flag
        return False
    # Open Colmap project from sparse as well as dense recon (fused.ply)
    print("Importing project")
    ms.load_project([base_path+r"\images\bundle.out", base_path+r'\images\bundle.out.list.txt'])
    if flag: 
        ~flag
        return False
    ms.load_new_mesh(base_path+r"\fused.ply")
    if flag: 
        ~flag
        return False
    
    print(ms.number_meshes())

    # Point cloud simplification
    print("Optimizing Point Cloud")
    ms.meshing_decimation_clustering(threshold = pymeshlab.AbsoluteValue(0.001))
    if flag: 
        ~flag
        return False

    # Mesher
    print("Starting Poisson Mesher")
    ms.generate_surface_reconstruction_screened_poisson(depth = 8, samplespernode = 20, pointweight = 4)
    if flag: 
        ~flag
        return False

    # Mesh simplification
    print("Optimizing Mesh")
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum = 500000, preserveboundary = True, preservenormal = True)
    if flag: 
        ~flag
        return False

    # Remove non-manifold edges
    print("Removing non-manifold edges")
    ms.meshing_repair_non_manifold_edges()
    if flag: 
        ~flag
        return False

    # Wipe verticies colors
    print("Setting vertex colors")
    ms.set_color_per_vertex(color1 = pymeshlab.Color(255, 255, 255))
    if flag: 
        ~flag
        return False

    # Build texture
    print("Building texture from registered rasters")
    ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = 1024, texturename = "newtexture.png")
    if flag: 
        ~flag
        return False

    # Export mesh
    print(f"Exporting mesh to ")
    ms.save_current_mesh(projdir + "landscape.obj")
    if flag: 
        ~flag
        return False

def kill():
    flag = True