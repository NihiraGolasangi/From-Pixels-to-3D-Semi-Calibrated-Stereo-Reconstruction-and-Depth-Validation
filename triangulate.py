
import numpy as np
from typing import Tuple
import cv2
from pathlib import Path

from intrinsic_params import get_intrinsic_matrix
from stereo_feature_matching import get_correspondences
from estimate_essential_pose import estimate_essential_and_pose


def triangulate_points(
    pts1: np.ndarray,
    pts2: np.ndarray,
    K: np.ndarray,
    R: np.ndarray,
    t: np.ndarray,
    inlier_mask: np.ndarray,
    baseline: float | None = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Triangulate 3‑D points given pose and intrinsics.

    Returns
    -------
    points3D : (N × 3)  – 3‑D coordinates in camera‑1 frame
    depths    : (N,)    – Z values == depth
    """
    # --- optional metric scaling ---
    if baseline is not None:
        t = baseline * t / np.linalg.norm(t)

    # --- projection matrices ---
    P1 = K @ np.hstack((np.eye(3), np.zeros((3,1))))
    P2 = K @ np.hstack((R, t))

    # --- keep inliers only ---
    mask = inlier_mask.ravel().astype(bool)
    pts1_in = pts1[mask]
    pts2_in = pts2[mask]

    # --- triangulate ---
    pts4D = cv2.triangulatePoints(P1, P2, pts1_in.T, pts2_in.T)  # 4×N
    pts3D = (pts4D[:3] / pts4D[3]).T                            # N×3
    depths = pts3D[:, 2]

    return pts3D, depths



#-----------
# Usage example
#-----------
if __name__ == "__main__":
    json_path = "LEFT/image_metadata.json"
    K = get_intrinsic_matrix(json_path)

    # Replace these with actual matched keypoints (pts1, pts2)
    left_img_path  = Path("LEFT/IMG_6404.jpg")
    right_img_path = Path("RIGHT/IMG_6414.jpg")

    pts1, pts2, matches, kpL, kpR = get_correspondences(
        left_img_path, right_img_path,
        top_N=150,               # how many matches for geometry
        ratio_thresh=0.75        # Lowe’s ratio
    )


    E, R, t, inliers = estimate_essential_and_pose(pts1, pts2, K)

    pts3D, depths = triangulate_points(pts1, pts2, K, R, t, inliers, baseline=0.36)

    print("Triangulated points:", pts3D.shape)
    print("Depth stats  (m): min =", depths.min(), "   max =", depths.max())

    # depths = pts3D[:, 2]
    # left_img_path = "/Users/nihiragolasangi/Developer/From-Pixels-to-3D-Semi-Calibrated-Stereo-Reconstruction-and-Depth-Validation/LEFT/IMG_6404.jpg"

    # # Load the left image (in color for visualization)
    # imgL = cv2.imread(left_img_path, cv2.IMREAD_COLOR)

    # # Find indices of min and max depth
    # min_idx = depths.argmin()
    # max_idx = depths.argmax()

    # # Coordinates of those points in image
    # min_pt = tuple(map(int, pts1[min_idx]))
    # max_pt = tuple(map(int, pts1[max_idx]))

    # # Convert grayscale to color if needed
    # if len(imgL.shape) == 2:
    #     img_vis = cv2.cvtColor(imgL, cv2.COLOR_GRAY2BGR)
    # else:
    #     img_vis = imgL.copy()

    # # Draw circles and labels
    # cv2.circle(img_vis, min_pt, radius=10, color=(0, 255, 0), thickness=3)  # green for min depth (closest)
    # cv2.putText(img_vis, "Min Depth", (min_pt[0]+10, min_pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # cv2.circle(img_vis, max_pt, radius=10, color=(0, 0, 255), thickness=3)  # red for max depth (farthest)
    # cv2.putText(img_vis, "Max Depth", (max_pt[0]+10, max_pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # # Show image
    # cv2.imshow("Min and Max Depth Points", img_vis)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()