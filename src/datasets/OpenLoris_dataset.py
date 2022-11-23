import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R

class OpenLorisDataset():
    """
    Pose Ground-Truth reader that conforms to the OpenLoris-Scene dataset format
    https://lifelong-robotic-vision.github.io/dataset/scene.html
    """
    
    # OpenLoris represents odometry as a 3x1 vector tx, ty, tz
    # and a quaternion qx, qy, qz, qw.
    OPENLORIS_COL_NAMES = [
        'time', 'tx', 'ty', 'tz',
        'qx', 'qy', 'qz', 'qw'
    ]

    OPENLORIS_ROT_COL_NAMES = [
        'qx', 'qy', 'qz', 'qw'
    ]

    OPENLORIS_R_VEC_COL_NAMES = ["x", "y", "z"]

    def read_file(self, input_file):
        poses = pd.read_csv(input_file, sep=' ', names=self.OPENLORIS_COL_NAMES)
        print(poses)
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
        rotations = poses[self.OPENLORIS_ROT_COL_NAMES].to_numpy().reshape(len(poses), 4)
        rotations = R.from_quat(rotations)
        rotations = rotations.as_euler('xyz', degrees=True) #* 180 / 3.14 #rad to deg
        rotations = pd.DataFrame(rotations, columns=self.OPENLORIS_R_VEC_COL_NAMES)
        print(rotations)
        return rotations[rotation_axis].to_numpy()

    