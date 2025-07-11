1. load images
2. detct keypoints and descriptors seperately for both imgaes
3. put the descriptors throught a match (knnmatcher)
4. apply lowe's ratio to get good matchees
5. select a few of these good matches for calculation



Totalculate essential matrix we are going to use :
E, mask = cv2.findEssentialMat(pts1, pts2, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
 so above are the steps to calcylate pts1 and pts2
