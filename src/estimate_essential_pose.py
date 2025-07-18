import cv2
import numpy as np
from typing import Tuple

from pathlib import Path

from intrinsic_params import get_intrinsic_matrix
from stereo_feature_matching import get_correspondences

def estimate_essential_and_pose(
    pts1: np.ndarray,
    pts2: np.ndarray,
    K: np.ndarray,
    ransac_prob: float = 0.999,
    ransac_thresh: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Estimate the Essential matrix and recover relative pose (R, t) between two views.

    Parameters
    ----------
    pts1 : np.ndarray (N × 2)
        Matched keypoints in image 1 (pixel coordinates)
    pts2 : np.ndarray (N × 2)
        Matched keypoints in image 2 (pixel coordinates)
    K : np.ndarray (3 × 3)
        Camera intrinsic matrix
    ransac_prob : float
        Confidence level for RANSAC (default = 0.999)
    ransac_thresh : float
        RANSAC reprojection threshold in pixels (default = 1.0)

    Returns
    -------
    E : np.ndarray (3 × 3)
        Estimated essential matrix
    R : np.ndarray (3 × 3)
        Relative rotation (from cam1 to cam2)
    t : np.ndarray (3 × 1)
        Relative translation (unit norm, from cam1 to cam2)
    inlier_mask : np.ndarray (N × 1)
        Boolean mask indicating which points are inliers
    """

    # 1. Estimate Essential Matrix using RANSAC
    E, inlier_mask = cv2.findEssentialMat(
        pts1, pts2, K,
        method=cv2.RANSAC,
        prob=ransac_prob,
        threshold=ransac_thresh
    )
    if E is None:
        raise RuntimeError("Essential matrix estimation failed.")

    # 2. Recover Pose from Essential Matrix
    _, R, t, pose_mask = cv2.recoverPose(E, pts1, pts2, K, mask=inlier_mask)

    # Combine masks if needed (here we trust pose_mask)
    inlier_mask = pose_mask.astype(bool).ravel()

    return E, R, t, inlier_mask


# Example usage
if __name__ == "__main__":


    # Dummy values for testing
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
    print("E:\n", E)
    print("R:\n", R)
    print("t:\n", t.ravel())
    print("Inliers:", inliers.sum(), "/", len(pts1))
