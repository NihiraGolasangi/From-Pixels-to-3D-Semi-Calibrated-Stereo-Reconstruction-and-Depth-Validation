## Essential Matrix

Here is a small recap of [Epipolar Geometry](epipolar_geometry.md)

We use 
- `pts1` and `pts2` : pixel coordinates of matching keypoints in left and right images. Shape is $N$x$2$ 
- `K` : Intrinsic Camera Matrix

to estimate the essential matrix.

We use a built-in fundtion `cv2.findEssentialMat()` to estimate the essential matrix and `cv2.recoverPose()` to recover rotational and translational matrix.

Now, why do we need to do this? - Answer to this is that we need the extrinsics of the system for triangulation (next step) and the ultimatly recover the depth.

Now, lets look at what these functions actually do?

## `cv2.findEssentialMat()`

Couple of high level steps that happen inside of `cv2.findEssentialMat()`:

### 1. Normalization
- Normalizes the image points using $K^{-1}$  to get normalized coordinates (rays).
### 2. Estimation algorithm - [5 point Algorithm](/steps/auxiliary.md#5---point-algorithm)
- Uses the 5-point algorithm to estimate $E$ from normalized correspondances.
-  5-point algorithm is an algorithm that uses It finds the Essential Matrix $E$ from 5 pairs of matching points.
    
** Finfing fundamnental matrix `cv2.findFundamentalMat()` uses 8-point algorithm to estimate $F$
### 3. Robust estimation with RANSAC - [RANSAC](/steps/auxiliary.md#ransac)
- Applies RANSAC to handle outliers (incorrect matches).
 - Randomly samples minimal sets, computes candidate $E$, and chooses the one with most inliers under the reprojection threshold.
### 4. Refinement
- After RANSAC finds the best model with inliers.
- It re-estimates the Essential Matrix using all inlier matches, typically via least squares.


Inliners: Inliers are those point correspondences between two images that fit well with the estimated model (Essential Matrix).


## `cv2.recoverPose()`

Steps inisde this function:

### 1. Decompose Essential Matrix using SVD
 Essential Mtrix satisfies 
 $$
 E = [t]_xR
 $$
  where $R$ is a rotational matrix and $[t]_x$ is a skew- symmetric matrix of $t$.
  Using Singular value decomposition: [Singular Value Decomposition](/steps/auxiliary.md#singular-value-decomposition)
  $$
  E= U \Sigma V^T
  $$
  From this, two possible rotations and two possible translations can be computed. So, there are four $(R, t)$ combinations.

 ### 2. Resolve Ambiguity via Cheirality Check

We get 4 possible camera poses from the decomposition.
To choose the correct one, we:

- Triangulate the 3D points for each (R, t) pair. [Triangulation](/steps/triangulation.md)

- Count how many of those 3D points lie in front of both cameras (i.e., have positive depth).

- The (R, t) pair with the maximum positive-depth points is chosen as the correct one.

This is called the cheirality condition — enforcing that points must be in front of the camera.