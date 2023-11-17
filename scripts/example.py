import os
from PIL import Image
import exifread

def extract_gps_from_image(image_path):
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

def extract_gps_from_directory(directory):
    gps_coordinates = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            image_path = os.path.join(directory, filename)
            gps_info = extract_gps_from_image(image_path)
            if gps_info:
                gps_coordinates[filename] = gps_info
    # returns a dict
    return gps_coordinates

images_directory = r'C:\Users\coden\Downloads\twin sisters'

if os.path.exists(images_directory):
    gps_data = extract_gps_from_directory(images_directory)
    if gps_data:
        for image, gps_info in gps_data.items():
            print(f"Image: {image}, GPS Coordinates: Latitude - {gps_info['latitude']}, Longitude - {gps_info['longitude']}")
    else:
        print("No GPS coordinates found in the images.")
else:
    print("The specified directory does not exist.")
