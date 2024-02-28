import os
from pathlib import Path

# List of allowed file types
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF']
DEFAULT_PREVIEW = Path(f"gui/placeholder/drone.jpg").resolve()

def get_num_img(imgdir):
    """
    Method returns the number of valid images in the image directory as an int. 
    Valid image types are: jpg, png, and tiff

    Args:
        imgdir (pathlib.Path): Image directory
    """
    numimg = 0
    for filename in os.listdir(imgdir):
        if filename.endswith(tuple(EXTENSIONS)):
            numimg += 1
    return numimg

def get_example_img(imgdir):
    """
    Gets the path for the first valid image in the image directory.

    Args:
        imgdir (pathlib.Path): Image directory
    """
    for filename in os.listdir(imgdir):
        if filename.endswith(tuple(EXTENSIONS)):
            return filename
    return DEFAULT_PREVIEW