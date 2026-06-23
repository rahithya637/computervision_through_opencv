import numpy as np
import cv2
from Ransac import *
from Affine import *


def extract_SIFT(img):

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Create SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors
    kp, desc = sift.detectAndCompute(img_gray, None)

    # Convert keypoints to numpy array
    kp = np.array([p.pt for p in kp]).T

    return kp, desc


def match_SIFT(descriptor_source, descriptor_target):

    bf = cv2.BFMatcher()

    # Find two nearest neighbors
    matches = bf.knnMatch(
        descriptor_source,
        descriptor_target,
        k=2
    )

    pos = np.array([], dtype=np.int32).reshape((0, 2))

    matches_num = len(matches)

    for i in range(matches_num):

        # Lowe ratio test
        if matches[i][0].distance <= 0.8 * matches[i][1].distance:

            temp = np.array([
                matches[i][0].queryIdx,
                matches[i][0].trainIdx
            ])

            pos = np.vstack((pos, temp))

    return pos


def affine_matrix(s, t, pos):

    # Select matched points
    s = s[:, pos[:, 0]]
    t = t[:, pos[:, 1]]

    # RANSAC to remove outliers
    _, _, inliers = ransac_fit(s, t)

    # Keep only inliers
    s = s[:, inliers[0]]
    t = t[:, inliers[0]]

    # Estimate affine matrix
    A, translation = estimate_affine(s, t)

    # Form 2x3 matrix
    M = np.hstack((A, translation))

    return M