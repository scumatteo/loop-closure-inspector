import argparse
import configparser
import sys

from datasets.KITTI_dataset import KITTIDataset
from datasets.OpenLoris_dataset import OpenLorisDataset
from datasets.TUM_dataset import TUMDataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')

def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog='LoopClosureInspector', 
        description='Python tool for loop closure ground truth labeling.')

    # Config File
    parser.add_argument(
        '--cfg', help='Configuration file path', required=True)

    args = parser.parse_args()
    
    cfg = configparser.ConfigParser()
    cfg.read(args.cfg)
    return cfg

def dataset_factory(use):
    if use == "KITTI":
        dataset = KITTIDataset()
      
    elif use == "OPENLORIS":
        dataset = OpenLorisDataset()

    elif use == "TUM":
        dataset = TUMDataset()
    
    return dataset

if __name__ == '__main__':
    cfg = parse_arguments(sys.argv)

    #read dataset
    dataset = dataset_factory(cfg["settings"]["use"])
    poses = dataset.read_file(cfg["settings"]["input-poses"])

    #get translations to draw
    translation_axis = cfg[cfg["settings"]["use"]]["translation_axis"].split(",")
    translations = dataset.get_translations(poses, translation_axis)

    #read pairs
    f_pairs = open(cfg["settings"]["input-pairs"])
    pairs = f_pairs.readlines()
    pairs = [pair.replace("\n", "") for pair in pairs]
    pairs = [tuple(map(int, pair.replace("(", "").replace(")", "").split(","))) for pair in pairs]

    #set indices to draw
    size = len(poses)
    loop_gt = np.zeros((size, size))

    for pair in pairs:
        if pair[0] != pair[1]:
            loop_gt[pair[0], pair[1]] = 1

    x = translations[:, [0]]
    y = translations[:, [1]]

    #plot the poses
    plt.plot(x, y)

    #plot the correspondences
    indices, _ = np.where(loop_gt > 0)
    x_coord = x[indices]
    y_coord = y[indices]
    plt.scatter(x_coord, y_coord, color = "red")
    plt.savefig("img.png")