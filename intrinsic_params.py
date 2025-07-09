import json




csv_path = '/Users/nihiragolasangi/Developer/From-Pixels-to-3D-Semi-Calibrated-Stereo-Reconstruction-and-Depth-Validation/LEFT/image_metadata.json'

with open(csv_path, 'r') as f:
    data = json.load(f)

def parse_fraction(value):
    try:
        if isinstance(value, str) and '/' in value:
            num, den = value.split('/')
            return float(num) / float(den)
        return float(value)
    except Exception:
        return None

def compute_intrinsic_matrix(image_width, image_height, focal_length_mm,equivalent_focal_length_mm,full_frame_diagonal = 43.3):

    crop_factor = equivalent_focal_length_mm / focal_length_mm 
    print(f"Crop factor: {crop_factor}")

    sensor_diagonal = full_frame_diagonal / crop_factor
    print(f"Sensor diagonal: {sensor_diagonal} mm")

    x = sensor_diagonal /5


    sensor_width_mm = 4* x
    sensor_height_mm = 3 * x
    print(f"Sensor width: {sensor_width_mm} mm, Sensor height: {sensor_height_mm} mm")

    f_x = (focal_length_mm * image_width) / sensor_width_mm
    f_y = (focal_length_mm * image_height) / sensor_height_mm
    c_x = image_width / 2
    c_y = image_height / 2
    K = [[f_x, 0, c_x],
         [0, f_y, c_y],
         [0, 0, 1]]
    return K


# Get first image's metadata without a loop
first_image_name, first_meta = next(iter(data.items()))

image_width = float(first_meta.get("ExifImageWidth", 0))
image_height = float(first_meta.get("ExifImageHeight", 0))
focal_length_mm = parse_fraction(first_meta.get("FocalLength"))
equivalent_focal_length_mm = parse_fraction(first_meta.get("FocalLengthIn35mmFilm"))
try:
    K = compute_intrinsic_matrix(image_width, image_height, focal_length_mm,equivalent_focal_length_mm)
    print(f"{first_image_name} Intrinsic Matrix:\n{K}\n")
except KeyError as e:
    print(f"Missing critical fields for {e}.")
