import os
import numpy as np
import pickle
import torch
import cv2
import matplotlib.pyplot as plt


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



def get_st_ed(batch_num):
    cumsum = torch.cumsum(batch_num, dim=0)
    st_ed = []
    for idx in range(1, cumsum.shape[0]):
        st_ed.append((int(cumsum[idx - 1]), int(cumsum[idx])))
    st_ed.insert(0, (0, int(cumsum[0])))
    return st_ed

def plot_trajectories(true_trajs, pred_trajs, obs_length, name, plot_directory, H_inv, background):

    data_len = 1
    fig, axes = plt.subplots(1, data_len)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

    # plt.subplots_adjust(bottom = 0.35, top = 0.95)
    ax = axes

    origin = true_trajs[0]
    true_trajs = true_trajs[1:]
    traj_length, numNodes, _ = true_trajs.shape

    width = 2
    height = 2

    traj_data = {}
    for tstep in range(obs_length, traj_length):
        pred_pos = pred_trajs[tstep, :]
        true_pos = true_trajs[tstep, :]

        for ped in range(numNodes):
            if ped not in traj_data:
                traj_data[ped] = [[], []]


            traj_data[ped][0].append(true_pos[ped, :])
            traj_data[ped][1].append(pred_pos[ped, :])


    # Ground Truth Trajectory
    ped_index = 0
    select_ped = [0]
    for j in traj_data:
        # if j not in select_ped:
        #     continue

        c = np.random.rand(3).tolist()

        true_traj_ped = traj_data[j][0]  # List of [x,y] elements
        pred_traj_ped = traj_data[j][1]
        if true_traj_ped == [] or pred_traj_ped == []:
            continue


        true_x = [p[0] for p in true_traj_ped]
        true_y = [p[1] for p in true_traj_ped]
        pred_x = [p[0] for p in pred_traj_ped]
        pred_y = [p[1] for p in pred_traj_ped]
        origin_x = [origin[j,0]]
        origin_y = [origin[j,1]]

        observed_x = origin_x + true_x[:7]
        observed_y = origin_y + true_y[:7]
        ground_truth_x = true_x[7:]
        ground_truth_y = true_y[7:]

        predicted_x = pred_x[7:]
        predicted_y = pred_y[7:]

        observed_trajectory = np.zeros((len(observed_x), 2))
        ground_truth_trajectory = np.zeros((len(ground_truth_x), 2))
        predicted_trajectory = np.zeros((len(predicted_x), 2))
        for i in range(len(observed_trajectory)):
            observed_trajectory[i][1] = observed_x[i]
            observed_trajectory[i][0] = observed_y[i]

        for i in range(len(ground_truth_trajectory)):
            ground_truth_trajectory[i][1] = ground_truth_x[i]
            ground_truth_trajectory[i][0] = ground_truth_y[i]
            predicted_trajectory[i][1] = predicted_x[i]
            predicted_trajectory[i][0] = predicted_y[i]

        observed_pixels = world2image(observed_trajectory, H_inv, background)  # observed_trajectory: Tx2 numpy array
        ground_truth_pixels = world2image(ground_truth_trajectory, H_inv, background)
        predicted_pixels = world2image(predicted_trajectory, H_inv, background)


        extent = [0, background.shape[1], background.shape[0], 0]

        ax.imshow(background, extent=extent, aspect='auto')
        ax.plot(observed_pixels[:,0], observed_pixels[:,1], color=c, linestyle='dotted', linewidth=5,
                label=f'true observed trajectory of {ped_index}')
        ax.plot(ground_truth_pixels[:,0], ground_truth_pixels[:,1], color=c, linestyle='solid', linewidth=5,
                label=f'true predicted trajectory of {ped_index}')
        ax.plot(predicted_pixels[:,0], predicted_pixels[:,1], color=c, linestyle='dashed', linewidth=5,
                label=f'predicted trajectory of {ped_index}')
        ax.scatter(ground_truth_pixels[-1,0], ground_truth_pixels[-1,1], color=c, marker='o', s=100,
                   label=f'ground truth endpoint of {ped_index}')
        ax.scatter(predicted_pixels[-1,0], predicted_pixels[-1,1], color=c, marker='*', s=100,
                   label=f'predicted endpoint of {ped_index}')

        ax.set_xlim([0, background.shape[1]])
        ax.set_ylim([background.shape[0], 0])

        ax.axis('off')
        # ax.axes.xaxis.set_visible(False)
        # ax.axes.yaxis.set_visible(False)


        # ax.axis('equal')
        ped_index += 1
    plt.tight_layout(pad=0)
    # plt.show()
    # print()
    # plt.savefig(plot_directory + '/' + name + '.png')



# choose your algorithm
algorithm_name = 'ours3'

# Dataset name
dataset_name = 'zara2'

# the path to store the generated trajectory and truth trajectory
save_directory = f'../save/{algorithm_name}/{dataset_name}/'

# load the homography matrix
H = (np.loadtxt(os.path.join(f'./{dataset_name}/H.txt')))
H_inv = np.linalg.inv(H)


# load background figure
background_image = cv2.imread(f'./{dataset_name}/889.png')
background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)


with open(save_directory + f'batch_pednum_{dataset_name}1.pkl', 'rb') as f:
    batch_pednum = pickle.load(f)
batch_pednum = batch_pednum['batch_pednum']
with open(save_directory + f'true_predicted_trajectory_{dataset_name}1.pkl', 'rb') as f:
    trajectory = pickle.load(f)
true_trajectory = trajectory['true_traj']
predicted_trajectory = trajectory['pred_traj']

# Plot directory (the plot of the trajectory is stored here)
plot_directory = f'./{dataset_name}/plot/{algorithm_name}'
if not os.path.exists(plot_directory):
    os.makedirs(plot_directory)

withBackground = 0
test_len = len(true_trajectory)
count = 0
pick_scene = [839]
for i in range(test_len):
    st_ed = get_st_ed(batch_pednum[i])
    len_st_ed = len(st_ed)
    for j in range(len_st_ed):
        print(count)
        name = 'scene' + str(count)
        st = st_ed[j][0]
        ed = st_ed[j][1]
        batch_true_trajectory = true_trajectory[i][:, st:ed, :]
        batch_predicted_trajectory = predicted_trajectory[i][:, st:ed, :]
        # plot_trajectories(batch_true_trajectory, batch_predicted_trajectory, 0, name, plot_directory,
        #                   H_inv, background_image)  # This is the core
        if count in pick_scene:
            plot_trajectories(batch_true_trajectory, batch_predicted_trajectory, 0, name, plot_directory,
                              H_inv, background_image)  # This is the core
        count += 1


