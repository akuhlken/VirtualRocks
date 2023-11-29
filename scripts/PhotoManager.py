import pathlib as pl
import exifread
import os

class PhotoManager():    

    def __init__(self, imgdir):
        self.metadict = {}
        self.numimg = 0
        self.imgdir = pl.Path(imgdir)
    
    # Helper function to get the GPS coords of a specific image
    def _extract_gps(self, imgpath):
        with open(imgpath, 'rb') as f:
            tags = exifread.process_file(f)
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                latitude = tags['GPS GPSLatitude']
                longitude = tags['GPS GPSLongitude']
                latref = tags['GPS GPSLatitudeRef']
                longref = tags['GPS GPSLongitudeRef']
                return {
                    'latitude': str(latitude) + ' ' + str(latref),
                    'longitude': str(longitude) + ' ' + str(longref)
                }
            else:
                return None

    # Sets the imgdict variable with a dictionary of metadata for each image
    #   Uses the filename as the key in the dict and the value is a GPS struct
    def make_dict(self):
        for filename in os.listdir(self.imgdir):
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                imgpath = os.path.join(self.imgdir, filename)
                gps = self._extract_gps(imgpath)
                if gps:
                    self.metadict[filename] = gps
                    self.numimg += 1