import shutil
import pymeshlab
import os
import sys

# Default Parameters
OVERLAP = 0.1 # Overlap ammount between tiles
TEXTURE_RES = 1024
CELL_SIZE = 0.0001 # Clustering decimation cell size
TILE_SIZE = 5000 # Will subdivide tiles until they are below this number of verts

class Mesher():

    def __init__(self, projdir):
        self.projdir = projdir
        self.dense2mesh()

    def dense2mesh(self):
        # Path to Colmap dense folder
        base_path = self.projdir + r"\dense"

        # Create a new MeshSet object
        print("---Loading pymeshlab---")
        self.ms = pymeshlab.MeshSet()
        self.ms.set_verbosity(False)
        
        # Open Colmap project from sparse as well as dense recon (fused.ply)
        print("---Importing project files---")
        self.ms.load_project([base_path+r"\images\project.bundle.out", base_path+r'\images\project.list.txt'])
        
        # Import the fused.ply mesh
        print("---Loading dense point cloud---")
        self.ms.load_new_mesh(base_path+r"\fused.ply")

        # Point cloud simplification
        print("---Optimizing Point Cloud---")
        self.ms.meshing_decimation_clustering(threshold = pymeshlab.AbsoluteValue(CELL_SIZE))
        
        # Mesher
        print("---Starting Poisson Mesher---")
        self.ms.generate_surface_reconstruction_screened_poisson(depth = 12, samplespernode = 20, pointweight = 4)

        # TODO: If model is empty try again with lower depth values until it works
        
        # Wipe verticies colors
        print("---Setting vertex colors---")
        self.ms.set_color_per_vertex(color1 = pymeshlab.Color(255, 255, 255))

        self.outdir = self.projdir + r"\out"
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)
        os.makedirs(self.outdir)

        print("---Computing model bounds---")
        min=self.ms.current_mesh().bounding_box().min()
        max=self.ms.current_mesh().bounding_box().max()

        minx = min[0] 
        maxx = max[0]
        miny = min[1]
        maxy = max[1]

        self.tile = 0
        self.fullmodel = self.ms.current_mesh_id()
        print("---Starting tiling---")
        self._quad_slice(maxx, minx, maxy, miny)

        print("---Finished tiling---")
        self.ms.set_current_mesh(self.fullmodel)
        
        #Mesh simplification
        print("---Creating low poly mesh---")
        self.ms.meshing_decimation_quadric_edge_collapse(targetfacenum = 100000, preserveboundary = True, preservenormal = True)

        # Remove non-manifold edges
        print("---Removing non-manifold edges---")
        self.ms.meshing_repair_non_manifold_edges()

        print("---Building texture for low poly mesh---")
        self.ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = "100k.jpg", usedistanceweight=False)
        # Export mesh
        print(fr"Exporting mesh to {self.outdir}\100k.obj")
        self.ms.save_current_mesh(fr"{self.outdir}\100k.obj")
        print("Done!")
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
            print(f"Building texture for land_{self.tile}.obj")
            self.ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = f"land_{self.tile}.jpg", usedistanceweight=False)

            # Export mesh
            print(fr"Exporting mesh to {self.outdir}\land_{self.tile}.obj")
            self.ms.save_current_mesh(fr"{self.outdir}\land_{self.tile}.obj")
            print()
            self.tile += 1
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

#projdir = sys.argv[1]
print("starting")
Mesher(r"C:\Users\akuhl\Downloads\testproj")
