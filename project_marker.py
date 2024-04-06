import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

# this script is for checking the calibration
# between camera and vicon system

def main():
    cam_ins_path = 'E:/ins_ext_parameters/p13/cam_ins.txt'
    cam_ext_path = 'E:/ins_ext_parameters/p13/vicon_to_cam.txt'
    path_3d = "E:/Vicon/chair/25-01/1.csv"
    path_img = "E:/radar_DATA/chair/25-01/2024-01-26-11-30-02/rgb/"
    cam_ins = np.loadtxt(cam_ins_path)
    cam_ext = np.loadtxt(cam_ext_path)
    xls3 = pd.read_csv(path_3d, skiprows=3)
    data_3d = xls3[1:].to_numpy(dtype=np.float64)
    marker3d = data_3d[:, 2:].mean(axis=0).reshape(6, 3)
    print("marker position in 3d:" + str(marker3d))

    project_3d_to_2d(marker3d, cam_ins, cam_ext, path_img)


def project_3d_to_2d(marker3d, cam_ins, cam_ext, path):
    mk3d_cam = cam_ext[:3, :3] @ marker3d.T + np.expand_dims(cam_ext[:3, 3], axis=1)
    uvw = cam_ins.dot(mk3d_cam)
    uvw /= uvw[2]
    uvs = uvw[:2].T
    print("calculated marker position in 2d:" + str(uvs))
    image_path = os.path.join(path, os.listdir(path)[0])
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.scatter(uvs[:, 0], uvs[:, 1], s=2.5, marker='o')
    plt.show()


if __name__ == '__main__':
    main()
