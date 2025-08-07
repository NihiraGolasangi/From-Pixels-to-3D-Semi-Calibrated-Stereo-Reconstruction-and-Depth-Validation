## Triangulation

Now that we have essential matrix, our stereo system is fully calibrated. We know the intrinsic and the extrinsic parameters of the system.

We use these know parameters to recover the depth of the 3D points. 

Triangulation is the method used to find the 3D position of a point using two or more 2D images of the scene.

## `triangulate_points()`

### 1. Metric Scaling
- The translational vector that we pass into this function that is originally derived from `cv2.recoverPose()` has unit length, so if we know the baseline distance we scale this vector to the scale. 

### 2. Build Projection Matrices
- We build two projection matrices: $P1$ and $P2$
- $P1 = K [I|0]$ camera 1 is the reference frame (camera 1 center is the origin)
- $P2 = k[R|t]$ Camera 2 projection matrix relative to camera 1

These matrices convert 3D points in the world into 2D pixel coordinates in the respective images.

### 3. Keep Inlier Matches Only
- Keep only the good matches (inliers from RANSAC) to ensure reliable triangulation. - Points that agree with teh essential matrix.

### 4. Triangulation
- Uses `cv2.triangulatePoints(P1, P2, pts1_in.T, pts2_in.T)` to triangulate. Here $P1,P2$ are projection matrices and $pts1_in$ and $pts2_in$ are the correspondences that agree with the estimated essential matrix.
- Mathematically, [Math Behind Triangulation](#math---triangulation)
- Outputs a $4*N$ matrix of homogeneous 3D points. Ecah column is $[X,Y,Z,W]^T$

5. Convert to Euclidean Coordinates
- Convert from homogeneous to Euclidean coordinates
- $[X,Y,Z,W]^T => [X/W , Y/W , Z/W]$

6. Extract Depths
- The Z-coordinate (depth) in camera 1's coordinate frame tells you how far each point is in front of the camera.




## Math - Triangulation
We have 
- Both camera's projectiom matrices 