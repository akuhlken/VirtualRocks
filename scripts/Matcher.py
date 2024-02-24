import os
import pathlib as pl
import shutil
import subprocess
import sys

class Matcher:
    
    def __init__(self, projdir, imgdir, clean):
        self.projdir = projdir
        self.imgdir = imgdir
        self.image2dense(clean) # TODO: clean arg should tell mesher wether to remove old db and folders

    # Main matcher pipeling code
    #   method should run all scripts accosiated with Colmap and result
    #   in a dense reconstruction
    def image2dense(self, clean):
        print("$$", flush=True)
        rcode = 0
        # clean old database
        try:
            database = self.projdir / pl.Path(r"database.db")
            if os.path.exists(database) and clean:
                os.remove(database)
                print("Removed old database", flush=True)
        except:
            rcode = 1
            print("Database already open (wait for old process to exit)", flush=True)

        # Colmap recon
        colmap = pl.Path("COLMAP.bat").resolve()
        workingdir = colmap.parent
        if rcode == 0:
            print("$Matcher.Feature Extractor.0$", flush=True)
            p = subprocess.Popen([str(colmap), "feature_extractor", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imgdir}"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0:
            print("$Matcher.Exhaustive Matching.17$", flush=True)
            p = subprocess.Popen([str(colmap), "exhaustive_matcher", "--database_path", f"{self.projdir}\database.db"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0:
            try:
                sparsedir = self.projdir / pl.Path(r"sparse")
                if os.path.exists(sparsedir) and clean:
                    shutil.rmtree(sparsedir)
                    print("Removed sparse", flush=True)
                if not os.path.exists(sparsedir):
                    os.makedirs(sparsedir)
                    print("Created sparse", flush=True)
            except:
                rcode = 1
                print("Files already open (wait for old process to exit)", flush=True)
        if rcode == 0:
            print("$Matcher.Mapper.33$", flush=True)
            p = subprocess.Popen([str(colmap), "mapper", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imgdir}", "--output_path", f"{self.projdir}\sparse"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0:
            try:
                densedir = self.projdir / pl.Path(r"dense")
                if os.path.exists(densedir):
                    shutil.rmtree(densedir)
                    print("Removed dense", flush=True)
                if not os.path.exists(densedir):
                    os.makedirs(densedir)
                    print("Created dense", flush=True)
            except:
                rcode = 1
                print("Files already open (wait for old process to exit)", flush=True)
        if rcode == 0:
            print("$Matcher.Image Undistorter.33$", flush=True)
            p = subprocess.Popen([str(colmap), "image_undistorter", "--image_path", f"{self.imgdir}", "--input_path", rf"{self.projdir}\sparse\0", "--output_path", f"{self.projdir}\dense", "--output_type", "COLMAP", "--max_image_size", "2000"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0:
            print("$Matcher.Dense Point Cloud Construction.50$", flush=True)
            p = subprocess.Popen([str(colmap), "patch_match_stereo", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--PatchMatchStereo.geom_consistency", "true"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0: 
            print("$Matcher.Stereo Fusion.67$", flush=True)
            p = subprocess.Popen([str(colmap), "stereo_fusion", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--input_type", "geometric", "--output_path", rf"{self.projdir}\dense\fused.ply"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0: 
            print("$Matcher.Model Converter.83$", flush=True)
            p = subprocess.Popen([str(colmap), "model_converter", "--input_path", rf"{self.projdir}\dense\sparse", "--output_path", f"{self.projdir}\dense\images\project", "--output_type", "Bundler"], cwd=str(workingdir), text=True)
            rcode = p.wait()
        if rcode == 0:
            print("$Matcher..100$", flush=True)

# Get args from the caller (recon manager)
projdir = sys.argv[1]
imgdir = sys.argv[2]
clean = True
if sys.argv[3] == 'F':
    clean = False
try:
    pass
    Matcher(projdir, imgdir, clean)
except Exception as e:
    print(e, flush=True)


