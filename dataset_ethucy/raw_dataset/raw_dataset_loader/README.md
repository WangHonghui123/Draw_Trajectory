# The loading of EWAP (ETH Walking Pedestrians Dataset) and UCY (Crowds-by-Example) Dataset

## Descriptions
The directory (raw_dataset_loader) is to load the raw dataset of EWAP (often referred as ETH) and UCY.

## Raw Datasets
The raw datasets of EWAP (ETH) and UCY is described as follows:

### EWAP (ETH)
The raw dataset is stored in the `obsmat.txt` file. Each line has this format:

#### Format
```
[frame_number pedestrian_ID pos_x pos_z pos_y v_x v_z v_y ]
```

however `pos_z` and `v_z` (direction perpendicular to the ground) are not used. The positions and velocities are in meters and are obtained with the homography matrix stored in H.txt .
Please note that we tried to avoid annotating those subjects that were at the border of the scene, as their behavior might have been influenced by the presence of other pedestrians/obstacles not in the field of view of the camera. We tried to be as consistent as possible in this regard. 

#### GROUPS
We tried to keep note of the people that seemed to walk in groups. These are listed in the file groups.txt . Each line contains a list of id, that are those that form a group. The id are the same as those in the obsmat.txt file 

#### DESTINATIONS
The assumed destinations for all the subjects walking in the scene are stored in the file destinations.txt . This is of course a simplifyiing assumption, but it seems to work fine for us.

#### OBSTACLES
the obstacles are reported in the map.png file. To bring the obstacle from image to world coordinates, the use of the homography matrix is necessary.

- **WARNING**: on 17/09/2009 the dataset have been modified, the frame number in the obsmat had a wrong offset (Thanks for corrections to Paul Scovanner)

#### How to load the raw dataset
In order to the load the datasets, we provided the `loader_eth.py`.

### UCY
The raw dataset is stored in the `annotation.vsp` file. 

#### Format
The tracked file consists of a series of splines that describe the moving behavior of a person in a video.
Comments in the file start with a '-' and end at the end of the line.

The number of splines can be found in the first line of the file.
Then immediately after that, each spline is defined in the following format:

```
   Number_of_control_points_N
   x y frame_number gaze_direction   \
   x y frame_number gaze_direction    \
   ....                                >>> N control points
   x y frame_number gaze_direction    /
   x y frame_number gaze_direction   /

   Number_of_control_points_K
   x y frame_number gaze_direction   \
   x y frame_number gaze_direction    \
   ....                                >>> K control points
   x y frame_number gaze_direction    /
   x y frame_number gaze_direction   /
   
   ....
   ...
```   
- `x, y`: the position of the person in pixel space, where (0, 0) is the center of the frame.
- `frame_number`: the time (frames)at which the position was tracked
- `gaze_direction`: the viewing direction of the person in degrees (0 degrees means the person is looking upwards)

#### How to load the raw dataset
In order to the load the datasets, we provided the `loader_crowds.py`.

Due to pixel coordinates in the original dataset, the corresponding homography matrix is used to obtain world coordinate.
`scipy.interpolate.interp1d` is used to interpolate for enriching the dataset.

* **Note**: The loader interpolates the annotated frames using linear interpolation. The framerate of annotations are then 2.5 fps (every 10 frames).

## License
No license information is available with this dataset.

## Citation
EWAP (ETH):
```
@inproceedings{pellegrini2009you,
  title={You'll never walk alone: Modeling social behavior for multi-target tracking},
  author={Pellegrini, Stefano and Ess, Andreas and Schindler, Konrad and Van Gool, Luc},
  booktitle={2009 IEEE 12th International Conference on Computer Vision},
  pages={261--268},
  year={2009},
  organization={IEEE}
}
```
UCY:
```
@inproceedings{lerner2007crowds,
  title={Crowds by example},
  author={Lerner, Alon and Chrysanthou, Yiorgos and Lischinski, Dani},
  booktitle={Computer graphics forum},
  volume={26},
  number={3},
  pages={655--664},
  year={2007},
  organization={Wiley Online Library}
}
```