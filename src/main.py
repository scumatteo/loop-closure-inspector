import argparse
import configparser
import sys
from datasets.KITTI_dataset import KITTIDataset
from datasets.OpenLoris_dataset import OpenLorisDataset
from datasets.TUM_dataset import TUMDataset
from distances.angular_distance import angular_distance_1D

import grispy as gsp
import os


import numpy as np


def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog='LoopClosureInspector', 
        description='Python tool for loop closure ground truth labeling.')

    # Config File
    parser.add_argument(
        '--cfg', help='Configuration file path', required=True)

    args = parser.parse_args()
    
    cfg = configparser.ConfigParser()
    cfg.read(args.cfg, encoding='utf8')
    return cfg

def dataset_factory(use):
    if use == "KITTI":
        dataset = KITTIDataset()
      
    elif use == "OPENLORIS":
        dataset = OpenLorisDataset()

    elif use == "TUM":
        dataset = TUMDataset()
    
    return dataset

def write(output_folder, pairs, dim):

    mat = np.zeros((dim, dim), dtype=np.int8)
    f = open(os.path.join(output_folder, "pairs.txt"), "a")
    for p in pairs:
        mat[p[0], p[1]] = 1
        f.write("(" + str(p[0]) + "," + str(p[1]) + ")\n")
    f.close()

    np.save("matrix.npy", mat)
    
    f = open(os.path.join(output_folder, "matrix.txt"), "a")
    for row in mat:
        f.write(str(row[0]))
        for i in range(1, len(row)):
            f.write(" " + str(row[i]))
        f.write("\n") 
            
if __name__ == '__main__':
    cfg = parse_arguments(sys.argv)

    #Load poses
    dataset = dataset_factory(cfg["settings"]["use"])
    poses = dataset.read_file(cfg["settings"]["input"])

    #parse params for the dataset
    section = cfg[cfg["settings"]["use"]]
    distance_lower_bound = float(section["distance_lower_bound"])
    distance_upper_bound = float(section["distance_upper_bound"])
    n_frame_since_last = int(section["n_frame_since_last"])
    translation_axis = section["translation_axis"].split(",")
    rotation_axis = section["rotation_axis"].split(",")
    max_angular_difference = int(section["max_angular_difference"])

    translations = dataset.get_translations(poses, translation_axis)
    print(translations)
    angles = dataset.get_angles(poses, rotation_axis)

    #euclidean distance to find the nn in a radius
    grid_translation = gsp.GriSPy(translations, N_cells=32, metric='euclid')
    near_translation_dist, near_translation_ind = grid_translation.shell_neighbors(translations, 
                                                                                    distance_lower_bound=distance_lower_bound, 
                                                                                    distance_upper_bound=distance_upper_bound)

    #for the nn found, a check on the temporal distance and the angle in done, to discard false loop closures
    good_pairs = []
    for i, idx in enumerate(near_translation_ind):
        if len(idx) > 1:
            for other in idx:
                if abs(other - i) > n_frame_since_last and angular_distance_1D(angles[i], [angles[other]], None) < max_angular_difference:
                    good_pairs.append((i, other))

    print("Found " + str(len(good_pairs)) + " correspondences!")

    write(cfg["settings"]["output"], good_pairs, len(poses))
            
    
    
    
    
