# Author: Javad Amirian
# Email: amiryan.j@gmail.com

import numpy as np
import pandas as pd
from trajdataset import TrajDataset
import os
import matplotlib.pyplot as plt



def load_eth(path, **kwargs):
    traj_dataset = TrajDataset()

    csv_columns = ["frame_id", "agent_id", "pos_x", "pos_z", "pos_y", "vel_x", "vel_z", "vel_y"]
    # read from csv => fill traj table
    raw_dataset = pd.read_csv(path, sep=r"\s+", header=None, names=csv_columns)

    traj_dataset.title = kwargs.get('title', "no_title")

    # copy columns
    traj_dataset.data[["frame_id", "agent_id",
                       "pos_x", "pos_y",
                       "vel_x", "vel_y"
                       ]] = \
        raw_dataset[["frame_id", "agent_id",
                     "pos_x", "pos_y",
                     "vel_x", "vel_y"
                     ]]

    traj_dataset.data["scene_id"] = kwargs.get('scene_id', 0)
    traj_dataset.data["label"] = "pedestrian"

    # post-process
    fps = kwargs.get('fps', -1)
    if fps < 0:
        d_frame = np.diff(pd.unique(raw_dataset["frame_id"]))
        fps = d_frame[0] * 2.5  # 2.5 is the common annotation fps for all (ETH+UCY) datasets

    sampling_rate = kwargs.get('sampling_rate', 1)
    use_kalman = kwargs.get('use_kalman', False)
    traj_dataset.postprocess(fps=fps, sampling_rate=sampling_rate, use_kalman=use_kalman)

    return traj_dataset


if __name__ == "__main__":
    # ETH (ETH and Hotel) dataset
    # =================================
    # It can choose ETH or Hotel dataset by changing the path
    eth_txt = os.path.join('../ETH/seq_eth/obsmat.txt')
    traj_dataset = load_eth(eth_txt)
    trajs = traj_dataset.get_trajectories()
    trajs = [(scene_id, agent_id, tr) for (scene_id, agent_id), tr in trajs]
    samples = traj_dataset.get_entries()
    plt.scatter(samples["pos_x"], samples["pos_y"])
    plt.show()
