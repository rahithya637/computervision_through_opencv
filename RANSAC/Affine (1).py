import numpy as np


def estimate_affine(s, t):
    num = s.shape[1]

    # Matrix M
    M = np.zeros((2 * num, 6))

    for i in range(num):
        temp = [
            [s[0, i], s[1, i], 0, 0, 1, 0],
            [0, 0, s[0, i], s[1, i], 0, 1]
        ]

        M[2 * i:2 * i + 2, :] = np.array(temp)

    # Target vector
    b = t.T.reshape((2 * num, 1))

    # Solve least squares
    theta = np.linalg.lstsq(M, b, rcond=None)[0]

    # Affine matrix
    X = theta[:4].reshape((2, 2))

    # Translation vector
    Y = theta[4:]

    return X, Y