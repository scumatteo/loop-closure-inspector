import pandas as pd
import numpy as np
from utils.rotations_utils import rotation_matrix_to_euler_angles

class KITTIDataset():
    """
    Pose Ground-Truth reader that conforms to the KITTI Odometry format
    http://www.cvlibs.net/datasets/kitti/eval_odometry.php
    """
    
    # KITTI represents odometry in 4x4 homogeneous pose matrices
    # and only writes the 3x3 rotation and 3x1 translation.
    # The missing row would be [0, 0, 0, 1]
    KITTI_COL_NAMES = [
        'r00', 'r01', 'r02', 'tx',
        'r10', 'r11', 'r12', 'ty',
        'r20', 'r21', 'r22', 'tz'
    ]

    KITTI_ROT_COL_NAMES = [
        'r00', 'r01', 'r02',
        'r10', 'r11', 'r12', 
        'r20', 'r21', 'r22'
    ]

    KITTI_R_VEC_COL_NAMES = ["x", "y", "z"]

    def read_file(self, input_file):
        poses = pd.read_csv(input_file, sep=' ', names=self.KITTI_COL_NAMES)
        return poses

    def get_translations(self, poses, translation_axis):
        """
        Returns the translations for the given axis.
        """
        return poses[translation_axis].to_numpy()

    def get_angles(self, poses, rotation_axis):
        """
        Returns the angles as Euler angles for the given axis.
        """
        rotations = poses[self.KITTI_ROT_COL_NAMES].to_numpy().reshape(len(poses), 3, 3)
        rotations = rotation_matrix_to_euler_angles(rotations) * 180 / 3.14 #rad to deg
        rotations = pd.DataFrame(rotations, columns=self.KITTI_R_VEC_COL_NAMES)
        return rotations[rotation_axis].to_numpy()

    