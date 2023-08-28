import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def save_image(image, num, save_directory):
  address = save_directory+ str(num) + '.png'
  cv2.imwrite(address, image)


# Dataset name
dataset_name = 'zara1'

# the path to store the frame extracted from the video
save_directory = f'./{dataset_name}/video_image/'

# the path to store the video file
video_file = f'./{dataset_name}/video.avi'

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# read the video file
videoCapture = cv2.VideoCapture(video_file)


# read the frame
success, frame = videoCapture.read()


i = 0
#set the fixed frame rate
timeF = 10
j=0
while success:
  i = i + 1
  if (i % timeF) == 0:
    # Create a new Matplotlib image
    fig, axes = plt.subplots()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    ax = axes
    extent = [0, frame.shape[1], frame.shape[0], 0]
    ax.imshow(frame, extent=extent, aspect='auto')
    ax.set_xlim([0, frame.shape[1]])
    ax.set_ylim([frame.shape[0], 0])
    plt.tight_layout(pad=0)
    # Convert Matplotlib image to NumPy array
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))  # 转换为RGB格式
    j = j + 1
    save_image(data, j, save_directory)
    print('save image:',j)
  success, frame = videoCapture.read()
