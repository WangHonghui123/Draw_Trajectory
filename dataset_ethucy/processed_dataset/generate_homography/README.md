# The description of generating homography matrix

## Homography
Homography matrics are provided by dataset creators in `H.txt` files in the `homography_matrix` directory. You can use them to project the world-coord positions (or trajectories) on the reference images (or videos).

`sgan_calculate_homography.py` is to generate homography matrix of UCY dataset only.

## Acknowledement
This script is from Scene-LSTM.

````
@inproceedings{huynh2019trajectory,
  title={Trajectory prediction by coupling scene-LSTM with human movement LSTM},
  author={Huynh, Manh and Alaghband, Gita},
  booktitle={Advances in Visual Computing: 14th International Symposium on Visual Computing, ISVC 2019, Lake Tahoe, NV, USA, October 7--9, 2019, Proceedings, Part I 14},
  pages={244--259},
  year={2019},
  organization={Springer}
}
````
