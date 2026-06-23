import numpy as np
import cv2
from Ransac import *
from Affine import *
from Align import *

# Read images
img_source = cv2.imread("2.jpg")
img_target = cv2.imread("target.jpg")

# Extract SIFT keypoints and descriptors
keypoint_source, descriptor_source = extract_SIFT(img_source)
keypoint_target, descriptor_target = extract_SIFT(img_target)

# Match descriptors
pos = match_SIFT(descriptor_source, descriptor_target)

# Compute affine transformation matrix
H = affine_matrix(keypoint_source, keypoint_target, pos)

# Get target image size
rows, cols, _ = img_target.shape

# Warp source image
warp = cv2.warpAffine(img_source, H, (cols, rows))

# Blend images
merge = np.uint8(img_target * 0.5 + warp * 0.5)

# Show result
cv2.imshow('Registered Image', merge)
cv2.waitKey(0)
cv2.destroyAllWindows()