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
**Given:**  
- Camera projection matrices:  
  $$
  P_1 \in \mathbb{R}^{3 \times 4}, \quad P_2 \in \mathbb{R}^{3 \times 4}
  $$  
- Corresponding 2D image points in homogeneous coordinates:  
  $$
  \mathbf{x}_1 = \begin{bmatrix} u_1 \\ v_1 \\ 1 \end{bmatrix} \in \mathbb{P}^2, \quad
  \mathbf{x}_2 = \begin{bmatrix} u_2 \\ v_2 \\ 1 \end{bmatrix} \in \mathbb{P}^2
  $$

Goal:  
Find the 3D homogeneous point  
$$ \mathbf{X} = [X, Y, Z, 1]^T \in \mathbb{P}^3 $$  
such that  
$$ \mathbf{x}_1 \sim P_1 \mathbf{X}, \quad \mathbf{x}_2 \sim P_2 \mathbf{X} $$


### Step 1: Cross product constraint

Because $ \mathbf{x}_i $ and $ P_i \mathbf{X} $ represent the same point up to scale, the cross product must be zero:  
$$ \mathbf{x}_1 \times (P_1 \mathbf{X}) = \mathbf{0}, \quad \mathbf{x}_2 \times (P_2 \mathbf{X}) = \mathbf{0} $$


### Step 2: Expand constraints into linear equations

Each cross product gives 3 equations, but only 2 are linearly independent. For each camera:  

$$
\begin{cases}
u_1 (P_1^{(3)} \mathbf{X}) - (P_1^{(1)} \mathbf{X}) = 0 \\
v_1 (P_1^{(3)} \mathbf{X}) - (P_1^{(2)} \mathbf{X}) = 0
\end{cases}
$$

$$
\begin{cases}
u_2 (P_2^{(3)} \mathbf{X}) - (P_2^{(1)} \mathbf{X}) = 0 \\
v_2 (P_2^{(3)} \mathbf{X}) - (P_2^{(2)} \mathbf{X}) = 0
\end{cases}
$$

where $ P_i^{(j)} $ is the $ j^{th} $ row of $ P_i $.


### Step 3: Construct linear system

Stack these into matrix form:  

$$ A \mathbf{X} = \mathbf{0} $$

where

$$
A = 
\begin{bmatrix}
u_1 P_1^{(3)} - P_1^{(1)} \\
v_1 P_1^{(3)} - P_1^{(2)} \\
u_2 P_2^{(3)} - P_2^{(1)} \\
v_2 P_2^{(3)} - P_2^{(2)}
\end{bmatrix}
$$

### Step 4: Solve for $ \mathbf{X} $

Use SVD to solve:  

$$ A = U \Sigma V^T \quad \Rightarrow \quad  \mathbf{X} = \mathbf{v}_4 $$

where $\mathbf{v}_4$ is the last column of $V$

Normalize $ \mathbf{X} $:

$$ \mathbf{X} \leftarrow \frac{\mathbf{X}}{X_4} $$


### Step 5: Repeat for all correspondences

Repeat this process for all pairs $$ (\mathbf{x}_1^{(i)}, \mathbf{x}_2^{(i)}) $$ to reconstruct all 3D points $$ \mathbf{X}^{(i)} $$.



