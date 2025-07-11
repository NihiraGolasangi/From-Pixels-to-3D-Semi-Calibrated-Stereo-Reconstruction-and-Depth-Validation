from pathlib import Path
import json
from typing import Dict, Any, List, Tuple, Optional


class ImageMetadata:
    """Lightweight wrapper around the EXIF‑like metadata of one image."""

    FULL_FRAME_DIAGONAL_MM = 43.3          # 36 mm × 24 mm sensor

    def __init__(self, meta: Dict[str, Any]) -> None:
        self.width_px:  float  = float(meta.get("ExifImageWidth", 0))
        self.height_px: float  = float(meta.get("ExifImageHeight", 0))
        self.focal_len_mm: float = self._parse_fraction(meta.get("FocalLength"))
        self.eq_focal_len_mm: float = self._parse_fraction(meta.get("FocalLengthIn35mmFilm"))

        self._assert_valid()

    # ---------- public helpers ---------- #
    def crop_factor(self) -> float:
        """35 mm‑equivalent focal ÷ actual focal."""
        return self.eq_focal_len_mm / self.focal_len_mm

    def sensor_diagonal_mm(self) -> float:
        """Physical diagonal of this camera’s sensor in millimetres."""
        return self.FULL_FRAME_DIAGONAL_MM / self.crop_factor()

    # ---------- internal utilities ---------- #
    @staticmethod
    def _parse_fraction(value: Any) -> float:
        """EXIF sometimes stores rational numbers as 'num/den' strings."""
        if value is None:
            return 0.0
        if isinstance(value, str) and "/" in value:
            num, den = value.split("/")
            return float(num) / float(den)
        return float(value)

    def _assert_valid(self) -> None:
        missing: List[str] = [
            name for name, v in {
                "width_px": self.width_px,
                "height_px": self.height_px,
                "focal_len_mm": self.focal_len_mm,
                "eq_focal_len_mm": self.eq_focal_len_mm,
            }.items() if v == 0
        ]
        if missing:
            raise ValueError(f"Missing required EXIF fields: {', '.join(missing)}")


class CameraIntrinsics:
    """Computes intrinsic matrix K for a pin-hole camera model."""

    def __init__(self, meta: ImageMetadata) -> None:
        self.meta = meta
        self.K: Optional[List[List[float]]] = None

    def compute(self) -> List[List[float]]:
        """
        Returns the 3x3 intrinsic matrix:
            [ f_x   0   c_x ]
            [  0   f_y  c_y ]
            [  0    0    1  ]
        """

        # --- derive physical sensor width & height from its diagonal (4:3 assumed) --- #
        diag = self.meta.sensor_diagonal_mm()
        # For a 4:3 sensor, diagonal = 5 units (4‑3‑5 triangle scaled)
        unit = diag / 5              # length of one 'unit'
        sensor_w_mm = 4 * unit
        sensor_h_mm = 3 * unit

        # --- focal lengths translated into pixel units --- #
        f_x = (self.meta.focal_len_mm * self.meta.width_px)  / sensor_w_mm
        f_y = (self.meta.focal_len_mm * self.meta.height_px) / sensor_h_mm
        c_x = self.meta.width_px  / 2.0
        c_y = self.meta.height_px / 2.0

        self.K = [[f_x, 0.0, c_x],
                  [0.0, f_y, c_y],
                  [0.0, 0.0, 1.0]]
        return self.K

    # convenient string representation
    def __repr__(self) -> str:     # pragma: no cover
        if self.K is None:         # compute lazily
            self.compute()
        rows = ["[" + ", ".join(f"{v:.2f}" for v in row) + "]" for row in self.K]
        return "K = " + "\n    ".join(rows)


# --------------------------------------------------------------------------- #
#  usage
# --------------------------------------------------------------------------- #
def load_metadata(json_path: str) -> Dict[str, dict]:
    with open(json_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    JSON_PATH = Path("/Users/nihiragolasangi/Developer/From-Pixels-to-3D-Semi-Calibrated-Stereo-Reconstruction-and-Depth-Validation/LEFT/image_metadata.json")
    all_meta = load_metadata(JSON_PATH)

    # Work with the first image in the file
    first_name, first_meta_dict = next(iter(all_meta.items()))
    meta = ImageMetadata(first_meta_dict)

    intrinsics = CameraIntrinsics(meta)
    K = intrinsics.compute()

    print(f"{first_name} intrinsic matrix:\n{intrinsics}")
