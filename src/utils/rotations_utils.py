import numpy as np
import cv2

def rotation_matrix_to_euler_angles(rotations):
    r_vecs = []

    for r in rotations:
        r_vec, _ = cv2.Rodrigues(r)
        r_vecs.append(r_vec[:, 0])

    r_vecs = np.array(r_vecs)
    return r_vecs