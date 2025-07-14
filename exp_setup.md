
### Experimental Setup and Depth Validation Methodology

This study investigates the feasibility of recovering accurate depth information from a stereo image pair acquired without explicit knowledge of the camera extrinsic parameters. The objective was to validate the depth estimates derived solely from image correspondences and intrinsic camera calibration.

#### Methodology:

1. **Intrinsic Calibration:**
   Camera intrinsic parameters, including focal length and principal point, were extracted from image metadata (EXIF tags). These parameters were utilized to construct the camera intrinsic matrix $\mathbf{K}$, essential for subsequent geometric computations.

2. **Feature Detection and Correspondence Establishment:**
   Distinctive local features were detected in the rectified stereo images using the Scale-Invariant Feature Transform (SIFT). Feature descriptors were matched using a brute-force k-nearest neighbors (k-NN) approach, followed by Lowe’s ratio test to eliminate ambiguous matches and ensure robust correspondences.

3. **Essential Matrix Estimation:**
   The essential matrix $\mathbf{E}$ was estimated from the matched keypoints and known intrinsic matrix $\mathbf{K}$, encoding the relative rotation $\mathbf{R}$ and translation $\mathbf{t}$ (up to scale) between the two camera poses.

4. **Pose Recovery and Triangulation:**
   The essential matrix was decomposed to yield four candidate relative poses. The correct pose was identified by enforcing the positive depth constraint on triangulated points. Subsequently, 3D point coordinates were reconstructed via triangulation of the matched image points using the recovered relative pose.

5. **Depth Validation:**
   The reconstructed 3D points’ depth values were statistically analyzed and compared against the approximate physical baseline and known scene geometry. The consistency of the depth range and distribution provided empirical validation of the reconstruction accuracy.

---

### Conclusion

The experiment demonstrates that it is possible to perform semi-calibrated stereo reconstruction, recovering relative camera pose and dense depth information from image correspondences and intrinsic calibration alone. This approach substantiates the viability of accurate depth estimation without direct extrinsic measurements, contributing valuable insights for applications in computer vision and 3D scene understanding.

