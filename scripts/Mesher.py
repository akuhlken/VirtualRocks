import shutil
import pymeshlab
import os
import sys

# VirtualRocks source is released under GPL-3.0-only or GPL-3.0-or-later

# Default Parameters
OVERLAP = 0.1 # Overlap ammount between tiles
TEXTURE_RES = 4096
CELL_SIZE = 0.0001 # Clustering decimation cell size
TILE_SIZE = 25000 # Will subdivide tiles until they are below this number of verts
VERTEX_LIMIT = 2000000
VERBOSE = False

class Mesher():

    def __init__(self, projdir):
        """
        `Mesher` is a python class designed to be run as a subprocess. It uses the 
        :ref:`pymeshlab <meshlab>` library to create the mesh, subdivide the mesh into tiles 
        until each tile has less than 50k verticies, generate textures, and create a low polygon
        mesh for the entire model.

        Args:
            projdir (pathlib.Path): Project directory containing .vrp file.
        """
        self.projdir = projdir
        self.dense2mesh()

    def dense2mesh(self):
        """
        Function to generate tiles with textures as well as a low poly mesh. After being started in
        main, it runs different :ref:`pymeshlab <meshlab>` functions while updating the progress
        bar for each one.
        """
        print("$$", flush=True)
        # Path to Colmap dense folder
        base_path = self.projdir + r"\dense"
    
        # Create a new MeshSet object
        print("$Mesher.Loading pymeshlab.0$", flush=True)
        self.ms = pymeshlab.MeshSet()
        self.ms.set_verbosity(VERBOSE)
    
        # Open Colmap project from sparse as well as dense recon (fused.ply)
        print("$Mesher.Importing project files.1$", flush=True)
        self.ms.load_project([base_path+r"\images\project.bundle.out", base_path+r'\images\project.list.txt'])
        if self.ms.mesh_number() != 1:
            raise Exception("Failed to load sparse point cloud with rasters")
        
        # Import the fused.ply mesh
        print("$Mesher.Loading dense point cloud.3$", flush=True)
        self.ms.load_new_mesh(base_path+r"\fused.ply")
        if self.ms.mesh_number() != 2:
            raise Exception("Failed to load dense point cloud")

        # Update bounding box for dense poit cloud
        self.bounds = self.ms.current_mesh().bounding_box()

        # Point cloud simplification
        print("$Mesher.Optimizing Point Cloud.5$", flush=True)
        self.ms.meshing_decimation_clustering(threshold = pymeshlab.PureValue(CELL_SIZE))

        # Mesher (this will retry with lower res if the user runs out of memory)
        print("$Mesher.Poisson Mesher.7$", flush=True)
        vertnum = 0
        depth = 12
        while vertnum < 100:
            self.ms.generate_surface_reconstruction_screened_poisson(depth = depth, samplespernode = 20, pointweight = 4)
            vertnum = self.ms.current_mesh().vertex_number()
            depth -= 1
        
        # Crop skirt from model
        self._crop()
        
        # Wipe verticies colors
        print("$Mesher.Setting vertex colors.18$", flush=True)
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

        print("$Mesher.Starting tiling.20$", flush=True)
        self.totalverts = self.ms.current_mesh().vertex_number()
        if self.totalverts > VERTEX_LIMIT:
            print(f"Reducing Mesh from {self.totalverts} to {VERTEX_LIMIT}", flush=True)
            self.ms.meshing_decimation_quadric_edge_collapse(targetfacenum = VERTEX_LIMIT, preserveboundary = True, preservenormal = True)
            print("Removing non-manifold edges", flush=True)
            self.ms.meshing_repair_non_manifold_edges()
            self.totalverts = self.ms.current_mesh().vertex_number()

        self.percentdone = 0.0
        self.tile = 0
        self.fullmodel = self.ms.current_mesh_id()
        self.ms.set_verbosity(False)
        self._quad_slice(minx, maxx, miny, maxy)
        print(f"Created {self.tile} tiles", flush=True)
        self.ms.set_current_mesh(self.fullmodel)
        self.ms.set_verbosity(VERBOSE)
        
        #Mesh simplification
        print("$Mesher.Creating low poly mesh.90$", flush=True)
        self.ms.meshing_decimation_quadric_edge_collapse(targetfacenum = 100000, preserveboundary = True, preservenormal = True)

        # Remove non-manifold edges
        print("Removing non-manifold edges", flush=True)
        nonman = self.ms.compute_selection_by_non_manifold_per_vertex()
        print(f"Found {nonman} non-manifold edges out of 100000 total vertices", flush=True)
        self.ms.meshing_repair_non_manifold_edges()

        print("Building texture for low poly mesh", flush=True)
        self.ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = "low_poly.jpg", usedistanceweight=False)
        # Export mesh
        print(fr"Exporting mesh to {self.outdir}\low_poly.obj", flush=True)
        self.ms.save_current_mesh(fr"{self.outdir}\low_poly.obj")
        print("$Mesher..100$", flush=True)
        print("$$", flush=True)
        return True
    
    def _quad_slice(self, minx, maxx, miny, maxy):
        """
        Recursive helper method for subdividing mesh into tiles. Once a tile is below 50k verticies,
        it generates a texture and export. The passed values allow the method to recurse on smaller
        portions of the mesh. Bounds are inclusive.

        .. note::
            Exported tiles save to the out folder in the current project directory. Their names
            follow the `"tile_#.obj"` format, where **#** is a number that distinguishes the tiles
            from each other.

        Args:
            minx (float): minimum x axis bound.
            maxx (float): maximum x axis bound.
            miny (float): minimum y axis bound.
            maxy (float): maximum y axis bound.
        """
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
            self.ms.compute_texcoord_parametrization_and_texture_from_registered_rasters(texturesize = TEXTURE_RES, texturename = f"tile_{self.tile}.jpg")

            # Export mesh
            self.ms.save_current_mesh(fr"{self.outdir}\tile_{self.tile}.obj")
            self.ms.set_selection_all()
            self.ms.meshing_remove_selected_vertices()
            # scaled_value = ((self.percentdone) * (70) / (100)) + 20
            self.tile += 1
            self.percentdone += numverts / self.totalverts * 100.0
            print(f"-----{round(self.percentdone, 2)}%", flush=True)
            print(f"$Mesher.Tiling.{int(((self.percentdone) * (70) / (100)) + 20)}$", flush=True)
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
        self._quad_slice(minx, midx, midy, maxy)

        # topright
        self._quad_slice(midx, maxx, midy, maxy)

        # bottomleft
        self._quad_slice(minx, midx, miny, midy)

        # bottomright
        self._quad_slice(midx, maxx, miny, midy)
        

    def _crop(self):
        """
        Helper function for cropping any extra points added to the mesh which lie outside the
        bounds of the original point cloud.
        """
        min=self.bounds.min()
        max=self.bounds.max()

        minx = min[0] 
        maxx = max[0]
        miny = min[1]
        maxy = max[1]

        self.ms.set_selection_none()
        self.ms.compute_selection_by_condition_per_vertex(condselect=f"(x < {minx} || x > {maxx}) || (y < {miny} || y > {maxy})")
        self.ms.meshing_remove_selected_vertices()

# Get args from caller (recon manager) and start mesher code
projdir = sys.argv[1]
try:
    Mesher(projdir)
except Exception as e:
    print(e, flush=True)