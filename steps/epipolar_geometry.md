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

