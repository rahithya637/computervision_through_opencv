import numpy as np
from Affine import *

K = 3
threshold = 1
ITER_NUM = 2000


def residual_lengths(X, Y, s, t):
    # Predicted points
    e = np.dot(X, s) + Y

    # Squared error
    diff_square = np.power(e - t, 2)

    # Euclidean distance
    residual = np.sqrt(np.sum(diff_square, axis=0))

    return residual


def ransac_fit(pts_s, pts_t):

    inliers_num = 0
    A = None
    t = None
    inliers = None

    for i in range(ITER_NUM):

        # Randomly choose 3 point pairs
        idx = np.random.randint(0, pts_s.shape[1], (K, 1))

        # Estimate affine parameters
        A_tmp, t_tmp = estimate_affine(pts_s[:, idx], pts_t[:, idx])

        # Compute residuals
        residual = residual_lengths(A_tmp, t_tmp, pts_s, pts_t)

        if residual is not None:

            # Find inliers
            inliers_tmp = np.where(residual < threshold)
            inliers_num_tmp = len(inliers_tmp[0])

            # Update best model
            if inliers_num_tmp > inliers_num:
                inliers_num = inliers_num_tmp
                inliers = inliers_tmp
                A = A_tmp
                t = t_tmp

    return A, t, inliers