import exifread
import os

# List of allowed file types
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF']

# TODO: Need to be a class?
class PhotoManager():    

    def __init__(self, imgdir):
        """
        description of the whole class

        Args:
            imgdir (path): what is it?
        """
        self.metadict = {}
        self.numimg = 0
        self.imgdir = imgdir
        self.num_images(imgdir)
    
    # Helper function to get the GPS coords of a specific image
    # TODO: remove method?
    def _extract_gps(self, imgpath):
        """
        description

        Args:
            imgpath (type?): what is it?
        """
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
        """
        description
        """
        for filename in os.listdir(self.imgdir):
            if filename.endswith(tuple(EXTENSIONS)):
                imgpath = os.path.join(self.imgdir, filename)
                gps = self._extract_gps(imgpath)
                if gps:
                    self.metadict[filename] = gps
        if not self.metadict:
            print("images do not have any GPS information")

    # Returns the number of valid images contained within the imgdir
    def num_images(self, imgdir):
        """
        description

        Args:
            imgdir (path): what is it?
        """
        self.numimg = 0
        for filename in os.listdir(imgdir):
            if filename.endswith(tuple(EXTENSIONS)):
                self.numimg += 1

    # Return the path to an image in the imgdir
    def get_example(self, imgdir=None):
        """
        description

        Args:
            imgdir (path): what is it?
        """
        if not imgdir:
            imgdir = self.imgdir
        for filename in os.listdir(imgdir):
            if filename.endswith(tuple(EXTENSIONS)):
                return filename