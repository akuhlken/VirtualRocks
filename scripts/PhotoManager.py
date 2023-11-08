from pprint import pprint
from PIL import Image
import piexif
import pathlib as pl

codec = 'ISO-8859-1'

class PhotoManager():    

    def __init__(self, imgDir):
        self.ImgMetaDict = {}
        self.MAX_LAT = -100
        self.MIN_LAT = 100
        self.MAX_LONG = -200
        self.MIN_LONG = 200
        self.NUM_IMGS = 0
        self.imgDir = pl.Path(imgDir)
        # dict of imgs + associated metadata

    def getNumImg(self):
        for path in pl.Path(self.imgDir).glob('*.jpg'):
            with open(str(path)) as f:
                self.NUM_IMGS += 1
        print("number of image loaded (PM): " + str(self.NUM_IMGS))

    def exif_to_tag(self, exif_dict):
        exif_tag_dict = {}
        thumbnail = exif_dict.pop('thumbnail')
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

#needed functions:
    # makeDict - makes the dictionary of images and their metadata. finds # of images, max lat + long values
    # getBounds - returns the min and max latitude and longitudes (as found in makeDict)
    # getNumImg - returns the number of images, as found by makeDict