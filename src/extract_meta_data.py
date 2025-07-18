from PIL import Image
from PIL.ExifTags import TAGS
import os
import json

def extract_metadata(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    metadata = {}
    
    if exif_data:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata[tag] = str(value)  # convert to string for JSON compatibility
    
    return metadata

metadata_dict = {}
folder_path = '/Users/nihiragolasangi/Developer/From-Pixels-to-3D-Semi-Calibrated-Stereo-Reconstruction-and-Depth-Validation/LEFT'
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".jpg"):
            full_path = os.path.join(folder_path, filename)
            metadata = extract_metadata(full_path)
            metadata_dict[filename] = metadata


output_path = os.path.join(folder_path, "image_metadata.json")
with open(output_path, "w") as f:
    json.dump(metadata_dict, f, indent=4)

print(f"Metadata - left saved to {output_path}")
    
#--------

metadata_dict = {}
folder_path = '/Users/nihiragolasangi/Developer/From-Pixels-to-3D-Semi-Calibrated-Stereo-Reconstruction-and-Depth-Validation/RIGHT'
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".jpg"):
            full_path = os.path.join(folder_path, filename)
            metadata = extract_metadata(full_path)
            metadata_dict[filename] = metadata


output_path = os.path.join(folder_path, "image_metadata.json")
with open(output_path, "w") as f:
    json.dump(metadata_dict, f, indent=4)

print(f"Metadata - right saved to {output_path}")