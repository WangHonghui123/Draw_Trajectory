# The generation of trajectories with background

## The generation of background

`plot_video_segment.py` is used to extract frames from video according to predefined frame rate.

## Plot the trajectories with background
The key to plot trajectories on the background (frames) is to convert
the location in the world coordinate to the pixel location via homography matrix.

```python
import os
import numpy as np
import cv2


def world2image(traj_w, H_inv, background):
    # Converts points from Euclidean to homogeneous space, by (x, y) → (x, y, 1)
    traj_homog = np.hstack((traj_w, np.ones((traj_w.shape[0], 1)))).T
    # to camera frame
    traj_cam = np.matmul(H_inv, traj_homog)
    # to pixel coords
    a = traj_cam[2]
    traj_uvz = np.transpose(traj_cam/a)
    traj_uv = traj_uvz[:, :2]
    return traj_uv[:, :2].astype(int)

# Dataset name
dataset_name = 'zara2'

# load the homography matrix
H = (np.loadtxt(os.path.join(f'./{dataset_name}/H.txt')))
H_inv = np.linalg.inv(H)

# load background figure
background_image = cv2.imread(f'./{dataset_name}/889.png')
background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)

# convert to the pixel location
# observed_trajectory: Tx2 numpy array: represent the location of observed trajectories in the world coordinate
observed_pixels = world2image(observed_trajectory, H_inv, background_image) 
```

The script for plotting trajectories with background (frame) extracted from the video is `plot_on_video.py`.

## Acknowledgement
The content largely borrows from OpenTraj benchmark.
```
@inproceedings{amirian2020opentraj,
      title={OpenTraj: Assessing Prediction Complexity in Human Trajectories Datasets}, 
      author={Javad Amirian and Bingqing Zhang and Francisco Valente Castro and Juan Jose Baldelomar and Jean-Bernard Hayet and Julien Pettre},
      booktitle={Asian Conference on Computer Vision (ACCV)},
      number={CONF},      
      year={2020},
      organization={Springer}
}
```

If you find this work useful in your research, please give a star to encourage me.
