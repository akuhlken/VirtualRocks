from pprint import pprint
from PIL import Image
import piexif
import pathlib as pl
import exifread
import os

codec = 'ISO-8859-1'

class PhotoManager():    

    def __init__(self, imgdir):
        self.ImgMetaDict = {}
        self.MAX_LAT = -100
        self.MIN_LAT = 100
        self.MAX_LONG = -200
        self.MIN_LONG = 200
        self.NUM_IMGS = 0
        self.imgdir = pl.Path(imgdir)
        # dict of imgs + associated metadata

    def getNumImg(self):
        for path in pl.Path(self.imgdir).glob('*.jpg'):
            with open(str(path)) as f:
                self.NUM_IMGS += 1
        print("number of image loaded (PM): " + str(self.NUM_IMGS))

    def exif_to_tag(self, exif_dict):
        exif_tag_dict = {}
        #print(exif_dict)
        thumbnail = exif_dict.pop('thumbnail')
        print(thumbnail)
        exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

        # for all of the elements in the metadata...
        for ifd in exif_dict:
            exif_tag_dict[ifd] = {}
            for tag in exif_dict[ifd]:
                try:
                    element = exif_dict[ifd][tag].decode(codec)
                    #print("good: " + str(piexif.TAGS[ifd][tag]["name"]) + " " + str(element))

                except AttributeError:
                    element = exif_dict[ifd][tag]
                    #print("bad: " + str(piexif.TAGS[ifd][tag]["name"]) + " " + str(element))

                exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

        return exif_tag_dict
    
    """
    def makeDict(self):
        # need to add img type support
        for path in pl.Path(self.imgDir).glob('*.jpg'):
            with open(str(path)) as f:
                self.NUM_IMGS += 1

                exif_dict = piexif.load(Image.open(path).info.get('exif'))
                exif = self.exif_to_tag(exif_dict)
                
                name = exif['0th']['ImageDescription']
                name = name.split("\\")[-1]

                self.ImgMetaDict[name] = exif['GPS']
                """

    def get_min_max_latlong(self):
        pass
    

    def extract_gps_from_image(self, image_path):
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                latitude = tags['GPS GPSLatitude']
                longitude = tags['GPS GPSLongitude']
                lat_ref = tags['GPS GPSLatitudeRef']
                lon_ref = tags['GPS GPSLongitudeRef']
                return {
                    'latitude': str(latitude) + ' ' + str(lat_ref),
                    'longitude': str(longitude) + ' ' + str(lon_ref)
                }
            else:
                return None

    def makeDict(self):
        for filename in os.listdir(self.imgdir):
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                image_path = os.path.join(self.imgdir, filename)
                gps_info = self.extract_gps_from_image(image_path)
                if gps_info:
                    self.ImgMetaDict[filename] = gps_info
                    self.NUM_IMGS += 1

#needed functions:
    # makeDict - makes the dictionary of images and their metadata. finds # of images, max lat + long values
    # getBounds - returns the min and max latitude and longitudes (as found in makeDict)
    # getNumImg - returns the number of images, as found by makeDict