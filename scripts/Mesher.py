import shutil
import pymeshlab
import os
import sys

# Default Parameters
OVERLAP = 0.1 # Overlap ammount between tiles
TEXTURE_RES = 1024
CELL_SIZE = 0.0001 # Clustering decimation cell size
TILE_SIZE = 50000 # Will subdivide tiles until they are below this number of verts
VERTEX_LIMIT = 2500000
VERBOSE = False

class Mesher():

    def __init__(self, projdir):
        self.projdir = projdir
        self.dense2mesh()

    def dense2mesh(self):
        # Path to Colmap dense folder
        base_path = self.projdir + r"\dense"
    
        # Create a new MeshSet object
        print("Loading pymeshlab.1", flush=True)
        self.ms = pymeshlab.MeshSet()
        self.ms.set_verbosity(VERBOSE)
    
        # Open Colmap project from sparse as well as dense recon (fused.ply)
        print("$Importing project files.1$", flush=True)
        self.ms.load_project([base_path+r"\images\project.bundle.out", base_path+r'\images\project.list.txt'])
        
        # Import the fused.ply mesh
        print("$Loading dense point cloud.1$", flush=True)
        self.ms.load_new_mesh(base_path+r"\fused.ply")

        # Update bounding box for dense poit cloud
        self.bounds = self.ms.current_mesh().bounding_box()

        # Point cloud simplification
        print("$Optimizing Point Cloud.1$", flush=True)
        self.ms.meshing_decimation_clustering(threshold = pymeshlab.AbsoluteValue(CELL_SIZE))

        # Mesher (this will retry with lower res if the user runs out of memory)
        print("$Starting Poisson Mesher.1$", flush=True)
        vertnum = 0
        depth = 12
        while vertnum < 100:
            self.ms.generate_surface_reconstruction_screened_poisson(depth = depth, samplespernode = 20, pointweight = 4)
            vertnum = self.ms.current_mesh().vertex_number()
            depth -= 1
        
        # Crop skirt from model
        self._crop()
        
        # Wipe verticies colors
        print("$Setting vertex colors.1$", flush=True)
        self.ms.set_color_per_vertex(color1 = pymeshlab.Color(255, 255, 255))

        self.outdir = self.projdir + r"\out"
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)
        os.makedirs(self.outdir)

        # Get model bounds
        min=self.ms.current_mesh().bounding_box().min()
        max=self.ms.current_mesh().bounding_box().max()

        minx = min[0] 
        maxx = max[0]
        miny = min[1]
        maxy = max[1]

        self.totalverts = self.ms.current_mesh().vertex_number()
        if self.totalverts > VERTEX_LIMIT:
            print(f"Reducing Mesh from {self.totalverts} to {VERTEX_LIMIT}", flush=True)
            self.ms.meshing_decimation_quadric_edge_collapse(targetfacenum = VERTEX_LIMIT, preserveboundary = True, preservenormal = True)
            print("Removing non-manifold edges", flush=True)
            self.ms.meshing_repair_non_manifold_edges()
            self.totalverts = self.ms.current_mesh().vertex_number()

        self.precentdone = 0.0
        self.tile = 0
        self.fullmodel = self.ms.current_mesh_id()
        self.ms.set_verbosity(False)
        print("$Starting tiling.1$", flush=True)
        self._quad_slice(maxx, minx, maxy, miny)

        print("$Finished tiling.1$", flush=True)
        print(f"Created {self.tile} tiles", flush=True)
        self.ms.set_current_mesh(self.fullmodel)
        self.ms.set_verbosity(VERBOSE)
        
        #Mesh simplification
        print("$Creating low poly mesh.1$", flush=True)
        self.ms.meshing_decimation_quadric_edge_collapse(targetfacenum = 100000, preserveboundary = True, preservenormal = True)

        # Remove non-manifold edges
        print("Removing non-manifold edges", flush=True)
        self.ms.meshing_repair_non_manifold_edges()

        print("Building texture for low poly mesh", flush=True)
        self.ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = "100k.jpg", usedistanceweight=False)
        # Export mesh
        print(fr"Exporting mesh to {self.outdir}\100k.obj", flush=True)
        self.ms.save_current_mesh(fr"{self.outdir}\100k.obj")
        print("$Done!.1$", flush=True)
        print("$$", flush=True)
        return True
    
    def _quad_slice(self, maxx, minx, maxy, miny):
        # Select verts in bounds
        self.ms.set_current_mesh(self.fullmodel)
        self.ms.set_selection_none()
        self.ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {maxx} && x > {minx}) && (y < {maxy} && y > {miny})")
        numverts = self.ms.current_mesh().selected_vertex_number()

        # Base Case (cut and export)
        if(numverts < TILE_SIZE):

            # Create new mesh with vertex within bounds + overlap
            self.ms.add_mesh(self.ms.mesh(self.fullmodel))
            self.ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {maxx + OVERLAP} && x > {minx - OVERLAP}) && (y < {maxy + OVERLAP} && y > {miny - OVERLAP})")
            self.ms.apply_selection_inverse()
            self.ms.meshing_remove_selected_vertices()

            # Build texture
            self.ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = f"land_{self.tile}.jpg", usedistanceweight=False)

            # Export mesh
            self.ms.save_current_mesh(fr"{self.outdir}\land_{self.tile}.obj")
            self.ms.set_selection_all()
            self.ms.meshing_remove_selected_vertices()

            self.tile += 1
            self.precentdone += numverts / self.totalverts * 100.0
            print(f"--{round(self.precentdone, 2)}%", flush=True)
            return

        """
                    maxy
                -----------
                |    |    |
           minx ----------- maxx
                |    |    |
                -----------
                    miny

        """
        midx = (maxx + minx) / 2.0
        midy = (maxy + miny) / 2.0

        # topleft
        self._quad_slice(midx, minx, maxy, midy)

        # topright
        self._quad_slice(maxx, midx, maxy, midy)

        # bottomleft
        self._quad_slice(midx, minx, midy, miny)

        # bottomright
        self._quad_slice(maxx, midx, midy, miny)
        

    # This will crop the current mesh to the bounds from the dense point cloud
    def _crop(self):
        min=self.bounds.min()
        max=self.bounds.max()

        minx = min[0] 
        maxx = max[0]
        miny = min[1]
        maxy = max[1]

        self.ms.set_selection_none()
        self.ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {minx} || x > {maxx}) || (y < {miny} || y > {maxy})")
        self.ms.meshing_remove_selected_vertices()
       

projdir = sys.argv[1]
# pass text file things are written to, args (this writes to something (text file) and then main would check it)
try:
    Mesher(projdir)
except Exception as e:
    print(e)
