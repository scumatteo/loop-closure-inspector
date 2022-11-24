# loop-closure-inspector

Package to create a ground truth for the Loop Closures in a map, given a ground truth of the poses.

# How it works
The tool detect a loop closure in 2D (for now), given a set of ground truth poses. 

For each pose, it checks if there are any poses closer than a certain radius. If there are any, for each of these it checks if the difference between the 1D orientations (with respect to the 2D plane) are less than a certain angle and if there is a minimum time span between the two poses.

If the above conditions are met, it means that there are two (or more) poses that have the same coordinates and the same orientation, so the robot (or the camera) retrace the same path moving in the same direction as in the past, effectively closing a loop.

The **distance_upper_bound** (the radius), the **max_angular_difference** (the angle) and the **n_frame_since_last** (the time span) must be set according to the dataset used. For example, for the KITTI dataset, that is an outdoor dataset, captured at 10fps with a car, the radius can be set to 1mt, the angle to 20° and the time span to 100 (100 frame at 10fps = 10seconds must be passed between two poses in order to consider them as a possible closure, in order to discard pose that are closer in space but captured too near in time, as for example if the camera is stationary in one point).


## Example

To a better understanding, consider the following example.

A ground truth for the poses is given, corresponding to the path below (the blue line). The arrow shows the direction of the robot while the red point is the pose to which the algorithm is searching a possible loop closure.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/loop.png?raw=true)

First, a search on a radius distance is done. So every point outside the red circle can be discarded.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/loop_radius.png?raw=true)

Second, a search on the orientation is done. Only the points inside the circle with the same orientation of the point are kept.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/loop_angle.png?raw=true)

Lastly, only the poses occurred after o before n frame are kept, in order to discard points that are close in time but not loop closures. The green poses are the candidates that can be considered loop closures for the red point.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/loop_final.png?raw=true)

## Negative example

Contrary to the previous example, in this case the robot returns to a place but it moves in the opposite direction (purple point). In this case, the loop closure is not detected.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/no_loop.png?raw=true)

# Requirements
To install the requirements use the following command:
```
pip install -r requirements.txt
```

This package uses **GriSPy** (https://github.com/mchalela/GriSPy) to perform an efficient search.

# How to use it
You can simply clone the repository and launch the *main.py* inside the folder */src/* with the command
```
python src/main.py --cfg /cfg/config.cfg --input /path/to/poses/ground/truth/ --output /path/to/output/folder
```

## Configurations
Inside the folder */cfg/* there are two files:
- **config.cfg** to set the configurations for the ground truth to create.
- **test.cfg** to display the ground truth created.

### config.cfg
This file contains the default settings for different datasets. 

Six parameters must be set, according to the dataset used:
- **distance_lower_bound** the lower bound for radius search in meters
- **distance_upper_bound** the upper bound for radius search in meters
- **n_frame_since_last** the number of frame that must occur between two loop closures
- **translation_axis** the axis to consider for the 2D loop closure
- **rotation_axis** the axis to consider for the angle
- **max_angular_difference** the maximum angle difference

### test.cfg
In this file, only the translation_axis are set, depending on the dataset, in order to display the results.

## Input
The input is the path to the ground truth of the poses.

## Outputs
It outputs three files:
- **matrix.npy** a matrix of shape NxN where N is the number of poses. Each cell contains 0 if the poses i,j are not considered loop closure, 1 if they are
- **matrix.txt** same as above
- **pairs.txt** a set of tuple with the indexes of the poses that are loop closures

## Test
To run the test, after the creation of the three outputs, the following command can be used
```
python src/test.py --cfg /cfg/test.cfg --input-pairs /path/to/output/pairs/ --input-poses /path/to/poses/ground/truth/
```

### Test with KITTI sequence 00
Example with the sequence 00 of the KITTI dataset. The red points are the poses in which the camera pass a second time, in the same direction. So they are the loop closures matches.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/kitti_00_loop.png?raw=true)

### Test with KITTI sequence 08
Example with the sequence 08 of the KITTI dataset. In this case the camera returns more times to the same places, but it moves with a different orientation, therefore no loop closure is detected.

![alt text](https://github.com/scumatteo/loop-closure-inspector/blob/main/img/kitti_08_loop.png?raw=true)




