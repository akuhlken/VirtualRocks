import os
from pathlib import Path

# List of allowed file types
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.JPG', '.JPEG', '.PNG', '.TIF', '.TIFF']
DEFAULT_PREVIEW = Path(f"gui/placeholder/drone.jpg").resolve()


def get_num_img(imgdir):
    """
    description

    Args:
        imgdir (path): what is it?
    """
    numimg = 0
    for filename in os.listdir(imgdir):
        if filename.endswith(tuple(EXTENSIONS)):
            numimg += 1
    return numimg

# Return the path to an image in the imgdir
def get_example_img(imgdir):
    """
    description

    Args:
        imgdir (path): what is it?
    """
    for filename in os.listdir(imgdir):
        if filename.endswith(tuple(EXTENSIONS)):
            return filename
    return DEFAULT_PREVIEW