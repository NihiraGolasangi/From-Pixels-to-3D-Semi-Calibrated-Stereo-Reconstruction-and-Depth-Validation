## Epipolar Geometry

Epipolar geometry is the geometry of two views of the same scene.

 **Epipoles** : Projection of the one camera center onto other camera's image plane.

 **Epipolar plane** : A plane that goes through the the left camera center, right camera center and the 3D point we are observing. Every 3D point has a unique epipolar plane.

 **Epipolar lines** : An epipolar line is the trace of, 3D points along a viewing ray emerging from one camera, onto other camera's image plane.

 Imagine we see a point $X_l$ in the left image. We define a ray from the lens of the left camera through this point $X_l$ into 3D space. Now, all the points on this ray, project to the same point $X_l$ in the left image. But when we project these 3D points onto the right image plane we see a line. This line is called as the epipolar line. 
 
Another way of looking at this is, eipolar line is the intersection of the epipoler plane (which is unique for every 3D point we observe) and the image plane.

## Epipolar constraint

This is simply an observation of the epipolar geometry. It is called a constraint because it restricts the possible location of a corresponding point in one image to lie on a specific line (the epipolar line) in the other image.

In other words, if the cameras are calibrated, the epipolar constraint guarantees that: For every point in the left image, the corresponding matching point in the right image must lie on a specific epipolar line.

This simple truth is easy to see once we understand the geometry well!

Now, let’s move to 3D space. The **epipolar plane** is defined by the centers of the two cameras and the 3D point we are observing. This means:
- The ray from the left camera center through $x_l$ lies in this plane.
- The rotated ray from the right camera center through $x_r$ also lies in this plane.
- The translation vector $t = C_r - C_l$ (between the two cameras) also lies in this plane.

To express this mathematically, we use the **scalar triple product**, which tells us whether three vectors are coplanar. Coplanarity is ensured when the triple product is zero:
$$
x_r^\top [t]_\times R x_l = 0
$$

Here:
-  $t$ cross  $R x_l$ = $[t]_x (R x_l)$ is a vector **perpendicular** to the epipolar plane. [Skew Symmetric matrix of a vector](/steps/auxiliary.md#skew-symmetric-matrix-of-a-vector)
- For $x_r$ to lie in the same plane, it must also be **perpendicular** to this vector, meaning their dot product must be zero.

(See the explanation of the [Scalar Triple Product](/steps/auxiliary.md#scalar-triple-product) for more details.)

### Note : Coordinate Frames of $x_l$ , $x_r$ , and $R x_l$

Let's take a quick check on what coordinate system these vectors are expressed in.

- $x_l$ is the normalized image point expressed as a ray **in the left camera’s coordinate system**.  Going from center of the left camera lens through the $(u_l,v_l)$ into the 3D space. $x_l$ is a $3$ x $1$ (in Homogeneous coordinates) direction vector. 
- $x_r$ is the corresponding normalized image point expressed as a 3D ray **in the right camera’s coordinate system**.  Going from center of the right camera lens through the $(u_r,v_r)$ into the 3D space. Dimensions are same as $x_l$
- To compare $x_l$ and $x_r$, we rotate $x_l$ using the rotation matrix $R$, so $R x_l$ is the vector $x_l$ **expressed in the right camera’s coordinate system**.  
- The translation vector $t$ from the left to right camera is also defined **in the right camera’s coordinate system**.  
- Therefore, in the epipolar constraint  
$$
x_r^\top [t]_\times R x_l = 0
$$  
  all vectors are expressed in the right camera frame.

Understanding that all these vectors are in 3D Euclidean space, which means 4D homogeneous coordinates. [Homogeneous Coordinates](/steps/auxiliary.md#homogeneous-coordinates)



## Essential Matrix

Now that we have the epipolar constaint mathematically expressed :
$$
x_r^\top [t]_\times R x_l = 0
$$

We define Essential Matrix $E$ as :
$$
E = [t]_\times R
$$

It conbines the extrinsics of the two camera positions : the relative rotation and translation between the two cameras in a $3$ x $3$ matrix!

With essential matrix the epipolar contraint can be rewritten as:

$$
x_r^TEx_l=0
$$

A key observation here is that Essential matrix because it is an encoding of rotation and translation between the two cameras , exists in physical (Euclidean) space. It operates on normalized image coordinates (rays), which we can only get if we know the intrinsic parameters of the cameras.

Now what if we donot know the intrisics of a camera? We cannot normalize the coordinates and hence connot use essential matrix directly.

To solve this problem we define a Fundamental matrix.

## Fundamental Matrix

We rewrite the epipolar contraint usinf fundamental matrix as: 
$$
U_r^TFU_l = 0
$$

Here $U_r$ and $U_l$ are unormalized image coordinates that are corresponding image points that match in the left and right image respectively.

Fundamental matrix encodes not just the extrinsics parameters but also instrinsic parameters into it. 

In terms of essesntial matrix, fundamental matrix can be written as:
$$
F = K_r^{-1}EK_l^{-1}
$$
Where , $K_r$ and $K_l$ are the intrisic matrices of right and left cameras respectively. [Normalization of image coordinates](/steps/auxiliary.md#normalization-of-image-coordinates)

