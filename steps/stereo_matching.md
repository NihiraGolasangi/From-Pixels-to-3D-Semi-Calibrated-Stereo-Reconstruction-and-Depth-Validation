# Stereo Matching - Flow

![Stereo matching flow](../images/stereo_matching_flow.png)



### 1. Loading images and converting to grayscale
- Left and right images are loaded.
- Converted to grayscale because for SIFT grayscale is enough - we donot need color. Hence to save computation we convert images to grayscale.
### 2. Detect Keypoints & Descriptors using SIFT
- Apply SIFT to both the left and right images.
- We detect:
    - `Keypoints` : Location of distinctive image features.
    - `Descriptors` : 128D feature vector describing each keypoint.

### 3. KNN Descriptor Matching (k=2)
- Perform k-nearest neighbor matching of descriptors using the L2 norm.
- For each descriptor in `img_left`, we find its 2 nearest matches in  `img_right`
- Here descriptor `d1` from left image will have two matches from the right image:
    - `m` : lowest distance from `d1` (best match)
    - `n` : second lowest distance from `d1` (second best match)


### 4. Lowe’s Ratio Test for Filtering
- We apply Lowe’s ratio test to remove ambiguous matches.

- `if m.distance < ratio_thresh * n.distance:`   then we keep the match. [`m` and `n` are two matches we got from KNN]
- The rationale is: if the best and second-best are too close, the match is ambiguous and likely unreliable.
- `ratio_thres` has a value of 0.75


### 5.  Select Top-N Matches (By Distance)
- From the filtered "good" matches, we select the top-N ones with the lowest distances (i.e., best quality matches).
- Essentially, Top-N matches are the N descriptor pairs (one from the left image and one from the right image) that:
    - Passed Lowe's ratio test (i.e., are likely good/valid matches), and
    - Have the smallest L2 distances between their descriptors.

### 6. Extract Matched Coordinates
- Converts the list of matches into two N × 2 arrays containing pixel coordinates of matching points:
    - `pts1` from the left image.
    - `pts2` from the right image.

- `cv2.Dmatch` object has attriutes :
    - `queryIdx` : index of the matched keypoint in the left image
    - `trainIdx` : index of the matched keypoint in the right image
- We use these attribute to construct `pts1` and `pts2`
- `kpL[m.queryIdx].pt` → returns (x, y) coordinate of the keypoint in the left image, `kpL` is the descriptor we got after applying SIFT
- Likewise for `kpR[m.trainIdx].pt` in the right image






