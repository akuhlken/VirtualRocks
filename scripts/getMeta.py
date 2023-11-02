from pprint import pprint
from PIL import Image
import piexif
import pathlib as pl

# class photoManager
# look at StartGUI for stuff about def __init__


# should be class with dictionary as a field, max lat long as field, min lat long as field

codec = 'ISO-8859-1'  # or latin-1

def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

def iterate(imgDir):
    print("hm, sux")
    # this is where i should loop through the images in the directory, passing the files from the directory to imgEXIF
    # end should return dictionary (or an object)
    # probably should make a dictionary of dictionaries.
    imagePath = pl.Path(imgDir + "/DJI_0441.jpg").resolve()
    imgEXIF(imagePath)


def imgEXIF(filename):
    # open the file
    im = Image.open(filename)
    # get the exif data from the image
    exif_dict = piexif.load(im.info.get('exif'))
    exif_dict = exif_to_tag(exif_dict)
    # print out the metadata to the terminal
    print(filename)
    pprint(exif_dict['GPS'])

    return

def main():
    # maybe loop with try except? easier way to look through everything in a folder?


    # use this, set to the folder that the input photos are saved to.
    filename_auto = pl.Path(f"TwinSisters/DJI_0458.jpg").resolve()

    filename = r"C:\Users\coden\OneDrive - Whitman College\Senior\Capstone\google earth\TwinSisters\DJI_0441.jpg"
    im = Image.open(filename)
    im2 = Image.open(filename_auto)

    exif_dict = piexif.load(im.info.get('exif'))
    exif_dict = exif_to_tag(exif_dict)

    print(filename)
    pprint(exif_dict['GPS'])

    exif_dict = piexif.load(im2.info.get('exif'))
    exif_dict = exif_to_tag(exif_dict)

    print(filename_auto)
    pprint(exif_dict['GPS'])

if __name__ == '__main__':
   main()