import os
from pathlib import Path

# List of allowed file types
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF']
DEFAULT_PREVIEW = Path(f"gui/placeholder/drone.jpg").resolve()

def get_num_img(imgdir):
    """
    Method returns the number of valid images `(see note above for valid types)` in the image
    directory as an int. 

    Args:
        imgdir (pathlib.Path): Path to image directory

    Returns:
        int: the number of valid images in the directory
    """
    numimg = 0
    for filename in os.listdir(imgdir):
        if filename.endswith(tuple(EXTENSIONS)):
            numimg += 1
    return numimg

def get_example_img(imgdir):
    """
    Gets the path for the first valid image in the given image directory. If theres no valid image
    in the image directory, then the method returns the path to the default preview image.

    Args:
        imgdir (pathlib.Path): Path to image directory
        
    Returns:
        pathlib.Path: path to preview image of image directory
    """
    for filename in os.listdir(imgdir):
        if filename.endswith(tuple(EXTENSIONS)):
            return filename
    return DEFAULT_PREVIEW