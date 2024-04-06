import json
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

camera_intrinsics_path = 'E:/ins_ext_parameters/p13/cam_ins.txt'
camera_extrinsics_path = 'E:/ins_ext_parameters/p13/vicon_to_cam.txt'

with open(camera_intrinsics_path, 'r') as f:
    intrinsics = np.array([line.strip().split() for line in f], dtype=float)
camera_matrix = intrinsics[:3, :3]

with open(camera_extrinsics_path, 'r') as f:
    extrinsics = np.array([line.strip().split() for line in f], dtype=float)
tvec = extrinsics[:3, 3]
rvec = extrinsics[:3, :3]

camera_extrinsics = np.eye(4)
camera_extrinsics[:3, :3] = rvec
camera_extrinsics[:3, 3] = tvec


def project_to_2d(points_3d, camera_matrix, camera_extrinsics):
    points_3d_homogeneous = np.hstack((points_3d, np.ones((points_3d.shape[0], 1))))
    points_camera = np.dot(camera_extrinsics, points_3d_homogeneous.T).T
    points_image_homogeneous = np.dot(camera_matrix, points_camera[:, :3].T).T
    points_2d = points_image_homogeneous[:, :2] / points_image_homogeneous[:, 2, np.newaxis]
    return points_2d


folder_rgb = 'E:/processed/p5/actions'
folder_json = 'E:/soma_parameter/p5'

# folder_json = 'E:/soma_parameter/p5_cut'

for i in range(1,51):
    json_path = os.path.join(folder_json, f'{i}.json')

    with open(json_path, 'r') as f:
        data = json.load(f)

    joints = data['joints']

    subfolder_name = str(i)
    subfolder_path = os.path.join(folder_rgb, subfolder_name, 'rgb')
    photos = sorted(os.listdir(subfolder_path), key=lambda x: int(os.path.splitext(x)[0]))
    photo_paths = [os.path.join(subfolder_path, photo) for photo in photos]

    current_frame = 0


    def update_frame(event):
        global current_frame
        if event.key == 'right' and current_frame < len(joints) - 2:
            current_frame += 2
        elif event.key == 'left' and current_frame > 0:
            current_frame -= 2
        else:
            return
        ax.clear()
        img = Image.open(photo_paths[0])
        print(photo_paths[0])

        # img = Image.open(photo_paths[current_frame])

        ax.imshow(img)
        points_3d = np.array(joints[current_frame])[:, :3]*1000
        points_2d = project_to_2d(points_3d, camera_matrix, camera_extrinsics)
        for x, y in points_2d:
            ax.plot(x, y, 'o', color='red', markersize=2)
        plt.title(f"Frame: {current_frame}; Action: {i}")
        fig.canvas.draw()


    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', update_frame)

    img = Image.open(photo_paths[0])
    ax.imshow(img)
    points_3d = np.array(joints[current_frame])[:, :3]*1000
    points_2d = project_to_2d(points_3d, camera_matrix, camera_extrinsics)
    for x, y in points_2d:
        ax.plot(x, y, 'o', color='red', markersize=2)

    plt.title(f"Frame: {current_frame}; Action: {i}")
    plt.show()

# import os
# subfolder_path = 'E:/radar_DATA/1/9/depth'
# files = [f for f in os.listdir(subfolder_path) if f.endswith('.png')]
# files_sorted = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))

# first_frame_number = int(os.path.splitext(files_sorted[0])[0])

# for f in files_sorted:
#     current_number = int(os.path.splitext(f)[0])
#     new_name = f"{current_number - first_frame_number}.png"
#     original_path = os.path.join(subfolder_path, f)
#     new_path = os.path.join(subfolder_path, new_name)

#     os.rename(original_path, new_path)