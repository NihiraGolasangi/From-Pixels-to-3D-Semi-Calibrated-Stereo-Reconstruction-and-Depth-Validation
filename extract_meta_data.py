from PIL import Image
from PIL.ExifTags import TAGS

def extract_focal_length(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == "FocalLength":
            return value

focal_length = extract_focal_length("/Users/nihiragolasangi/Developer/From-Pixels-to-3D-Semi-Calibrated-Stereo-Reconstruction-and-Depth-Validation/RIGHT/IMG_6423.jpg")
print("Focal length:", focal_length)
