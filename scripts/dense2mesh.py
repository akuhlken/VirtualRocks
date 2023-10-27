import pymeshlab

def colmap2mesh():
    # Path to Colmap dense folder
    base_path = r"C:\Users\chhengy\Downloads\miniproject-colmap\dense"

    # Create a new MeshSet object
    ms = pymeshlab.MeshSet()

    # Open Colmap project from sparse as well as dense recon (fused.ply)
    ms.load_project([base_path+r"\images\bundle.out", base_path+r'\images\bundle.out.list.txt'])
    ms.load_new_mesh(base_path+r"\fused.ply")

    # Point cloud simplification
    ms.meshing_decimation_clustering(threshold = pymeshlab.AbsoluteValue(0.001))

    # Mesher
    ms.generate_surface_reconstruction_screened_poisson(depth = 8, samplespernode = 20, pointweight = 4)

    # Mesh simplification
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum = 500000, preserveboundary = True, preservenormal = True)

    # Remove non-manifold edges
    ms.meshing_repair_non_manifold_edges()

    # Wipe verticies colors
    ms.set_color_per_vertex(color1 = pymeshlab.Color(255, 255, 255))

    # this dumps my core...
    # https://pymeshlab.readthedocs.io/en/latest/filter_list.html#compute_texcoord_parametrization_and_texture_from_registered_rasters
    ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = 1024, texturename = "newtexture.png")

    ms.save_current_mesh(r"C:\Users\chhengy\Downloads" + r"\test_export.obj")

    print(ms.number_meshes())  # if all is well this should give 3
    
colmap2mesh()