import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List

# -------------------------------------------------
# 1. Load images
# -------------------------------------------------
def load_grayscale_images(left_path: str, right_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load two images in grayscale.

    Returns
    -------
    img_left  : np.ndarray  (H × W)
    img_right : np.ndarray  (H × W)
    """
    img_left  = cv2.imread(str(left_path),  cv2.IMREAD_GRAYSCALE)
    img_right = cv2.imread(str(right_path), cv2.IMREAD_GRAYSCALE)
    if img_left is None or img_right is None:
        raise FileNotFoundError("Could not load one or both images.")
    return img_left, img_right


# -------------------------------------------------
# 2. Detect keypoints & descriptors (SIFT)
# -------------------------------------------------
def detect_features_sift(image: np.ndarray, n_features: int = 5000):
    """
    Detect SIFT keypoints & descriptors.

    Returns
    -------
    keypoints  : list[cv2.KeyPoint]
    descriptors: np.ndarray (N × 128)
    """
    sift = cv2.SIFT_create(nfeatures=n_features)
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors


# -------------------------------------------------
# 3. Match descriptors with KNN (k = 2)
# -------------------------------------------------
def knn_match(des1: np.ndarray, des2: np.ndarray, k: int = 2):
    """
    Brute‑Force matcher with L2 norm (default for SIFT descriptors).
    Returns list of k‑NN matches for every descriptor in des1.
    """
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=k)
    return matches


# -------------------------------------------------
# 4. Lowe’s ratio test
# -------------------------------------------------
def filter_matches_ratio(matches, ratio_thresh: float = 0.75):
    """
    Keep matches where best distance < ratio * second‑best distance.
    """
    good = [m for m, n in matches if m.distance < ratio_thresh * n.distance]
    return good


# -------------------------------------------------
# 5. Pick top‑N good matches (optional helper)
# -------------------------------------------------
def select_top_matches(good_matches, N: int = 100):
    """
    Sort good matches by distance and take the first N.
    """
    good_sorted = sorted(good_matches, key=lambda m: m.distance)
    return good_sorted[:N]


# -------------------------------------------------
# Utility: extract matched (u, v) coordinates
# -------------------------------------------------
def get_matched_points(kp1, kp2, matches) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert DMatch list -> two (N × 2) float32 arrays of pixel coordinates.
    """
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    return pts1, pts2


# ---------------------------------------------------
# Visulaize only top 5 matches with thick lines
# ----------------------------------------------------
# ----- 8. visualize only top 5 matches with thicker lines -----
def draw_top_matches_thick(img1, kp1, img2, kp2, matches, top_n=5, line_thickness=3,save_path=None):
    matches = sorted(matches, key=lambda m: m.distance)[:top_n]

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    out_img = cv2.hconcat([img1, img2])
    out_img = cv2.cvtColor(out_img, cv2.COLOR_GRAY2BGR)  # convert grayscale to BGR for colored drawing

    for m in matches:
        pt1 = tuple(map(int, kp1[m.queryIdx].pt))
        pt2 = tuple(map(int, (kp2[m.trainIdx].pt[0] + w1, kp2[m.trainIdx].pt[1])))  # offset pt2 x by width of img1

        # Draw keypoints as green circles
        cv2.circle(out_img, pt1, 5, (0, 255, 0), -1)
        cv2.circle(out_img, pt2, 5, (0, 255, 0), -1)

        # Draw thick blue line between matched points
        cv2.line(out_img, pt1, pt2, (255, 0, 0), thickness=line_thickness)
    if save_path:
        cv2.imwrite(save_path, out_img)
        print(f"Saved visualization to {save_path}")

    cv2.imshow(f"Top {top_n} Matches Thick Lines", out_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# -------------------------------------------------
#  HIGH‑LEVEL CONVENIENCE: get_correspondences
# -------------------------------------------------
def get_correspondences(
    left_path: str | Path,
    right_path: str | Path,
    top_N: int = 150,
    ratio_thresh: float = 0.75
) -> Tuple[np.ndarray, np.ndarray, List[cv2.DMatch], List[cv2.KeyPoint], List[cv2.KeyPoint]]:
    """
    End‑to‑end pipeline:
        1) load two images (grayscale)
        2) detect SIFT keypoints & descriptors
        3) knnMatch + Lowe's ratio test
        4) keep N best matches by distance
        5) return matched pixel coordinates ready for Essential‑matrix estimation

    Parameters
    ----------
    left_path, right_path : str | Path
        File paths to the left / right images.
    top_N : int
        How many of the best (lowest‑distance) matches to keep.
    ratio_thresh : float
        Lowe's ratio test threshold (default 0.75).

    Returns
    -------
    pts1 : np.ndarray (N × 2)
        Pixel coordinates from the left image.
    pts2 : np.ndarray (N × 2)
        Corresponding pixel coords from the right image.
    top_matches : list[cv2.DMatch]
        The DMatch objects for the kept correspondences.
    kpL, kpR : list[cv2.KeyPoint]
        Keypoints for left and right images (useful for visualization).
    """
    # --- 1. load grayscale images ---
    imgL, imgR = load_grayscale_images(str(left_path), str(right_path))

    # --- 2. detect SIFT features ---
    kpL, desL = detect_features_sift(imgL)
    kpR, desR = detect_features_sift(imgR)

    if desL is None or desR is None:
        raise RuntimeError("No descriptors found in one or both images.")

    # --- 3. match descriptors with 2‑NN ---
    knn_matches = knn_match(desL, desR, k=2)

    # --- 4. Lowe’s ratio filter ---
    good_matches = filter_matches_ratio(knn_matches, ratio_thresh=ratio_thresh)

    if len(good_matches) < top_N:
        print(f"[Warning] Only {len(good_matches)} good matches, less than requested {top_N}")

    # --- 5. sort by distance & keep top N ---
    top_matches = select_top_matches(good_matches, N=top_N)

    # --- 6. convert to coordinate arrays ---
    pts1, pts2 = get_matched_points(kpL, kpR, top_matches)

    return pts1, pts2, top_matches, kpL, kpR


# -------------------------------------------------
# Demo / CLI
# -------------------------------------------------
if __name__ == "__main__":
    left_img_path  = Path("LEFT/IMG_6404.jpg")
    right_img_path = Path("RIGHT/IMG_6414.jpg")

    pts1, pts2, matches, kpL, kpR = get_correspondences(
        left_img_path, right_img_path,
        top_N=150,               # how many matches for geometry
        ratio_thresh=0.75        # Lowe’s ratio
    )

    print("pts1 shape:", pts1.shape, "pts2 shape:", pts2.shape)

    # quick visualization of the best 5
    draw_top_matches_thick(
        cv2.imread(str(left_img_path), cv2.IMREAD_GRAYSCALE),
        kpL,
        cv2.imread(str(right_img_path), cv2.IMREAD_GRAYSCALE),
        kpR,
        matches,
        top_n=5,
        line_thickness=10,
        save_path="results/STEREO_FEATURE_MATCHING_TOP_05.jpg"
    )

    

