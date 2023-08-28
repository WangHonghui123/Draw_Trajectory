# The description of two directories.

These two directories seem to be from trajnet benchmark initially. 
But the website is not working.

Note that the data in two directories are same.

## `dataset_sgan` 
This directory stores the processed eth/ucy datasets,
and these are divided into `train/val/test` datasets via leave-one-out approach.

The first algorithm to use this dataset for pedestrian trajectory prediction is SGAN.

## `dataset_srlstm`
This directory stores the processed eth/ucy datasets, 
but these are NOT divided into `train/val/test` datasets via leave-one-out approach.

The first algorithm to use this dataset for pedestrian trajectory prediction is SR-LSTM.

### Citation
SGAN:
````
@inproceedings{gupta2018social,
  title={Social gan: Socially acceptable trajectories with generative adversarial networks},
  author={Gupta, Agrim and Johnson, Justin and Fei-Fei, Li and Savarese, Silvio and Alahi, Alexandre},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={2255--2264},
  year={2018}
}
````
SR-LSTM
```
@inproceedings{zhang2019sr,
  title={Sr-lstm: State refinement for lstm towards pedestrian trajectory prediction},
  author={Zhang, Pu and Ouyang, Wanli and Zhang, Pengfei and Xue, Jianru and Zheng, Nanning},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={12085--12094},
  year={2019}
}
```