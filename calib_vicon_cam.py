import numpy as np
import cv2
import pandas as pd

def main():
    cam_ins = np.array([[375.66860062, 0., 319.99508973],
                        [0., 375.66347079, 239.41364796],
                        [0., 0., 1.]])

    radar2rgb_tvec = np.array([-0.03981857, 1.35834002, -0.05225502])
    radar2rgb_rotmatrix = np.array([[9.99458797e-01, 3.28646073e-02, 1.42475954e-03],
                                    [4.78233954e-04, 2.87906567e-02, -9.99585349e-01],
                                    [-3.28919997e-02, 9.99045052e-01, 2.87593582e-02]])

    marker2d = np.zeros((6, 2))
    mat2d = [[329.500000000000,	322.500000000000, 0, 0],
            [295.500000000000,	295.500000000000, 0, 0],
            [295.500000000000,	343.500000000000, 0, 0],
            [315.500000000000,	359.500000000000, 0, 0],
            [320.500000000000,	369.500000000000, 0, 0],
            [282.500000000000,	359.500000000000, 0, 0]]

    for i in range(6):
        marker2d[i, 0] = mat2d[i][0] + mat2d[i][2] / 2
        marker2d[i, 1] = mat2d[i][1] + mat2d[i][3] / 2

    print("marker position in 2d:\n" + str(marker2d))

    path_3d = "E:/Vicon/chair/25-01/1.csv"
    xls3 = pd.read_csv(path_3d, skiprows=3)
    data_3d = xls3[1:].to_numpy(dtype=np.float64)
    marker3d = data_3d[:, 2:].mean(axis=0).reshape(6, 3)
    print("marker position in 3d:\n" + str(marker3d))

    retval, rvec, tvec = cv2.solvePnP(marker3d, marker2d, cam_ins, None)
    vicon_to_cam = np.eye(4)
    rot_mat, _ = cv2.Rodrigues(rvec)
    vicon_to_cam[:3, :3] = rot_mat
    vicon_to_cam[:3, 3] = tvec.squeeze(1)
    print("camera extrinsics:\n" + str(vicon_to_cam))

    np.savetxt("E:/ins_ext_parameters/p13/vicon_to_cam.txt", vicon_to_cam)
    np.savetxt("E:/ins_ext_parameters/p13/cam_ins.txt", cam_ins)
    np.savetxt("E:/ins_ext_parameters/p13/radar2rgb_tvec.txt", radar2rgb_tvec)
    np.savetxt("E:/ins_ext_parameters/p13/radar2rgb_rotmatrix.txt", radar2rgb_rotmatrix)


if __name__ == '__main__':
    main()
