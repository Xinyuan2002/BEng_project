import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

image_width = 640
image_height = 480

gb_matrix = np.array([[375.66860062, 0., 319.99508973],
                      [0., 375.66347079, 239.41364796],
                      [0., 0., 1.]])

radar2rgb_tvec = np.array([-0.03981857, 1.35834002, -0.05225502])
radar2rgb_rotmatrix = np.array([[9.99458797e-01, 3.28646073e-02, 1.42475954e-03],
                                [4.78233954e-04, 2.87906567e-02, -9.99585349e-01],
                                [-3.28919997e-02, 9.99045052e-01, 2.87593582e-02]])

CAM_EXT = np.eye(4)
CAM_EXT[:3, :3] = radar2rgb_rotmatrix
CAM_EXT[:3, 3] = radar2rgb_tvec

CAM_INS = gb_matrix

rgb_folder = 'E:/test/test/2024-01-19-21-14-10/rgb/'
mat_folder = 'E:/test/test/2024-01-19-21-14-10/mmwave/'
output_folder = 'E:/test/test/2024-01-19-21-14-10/test/'


def project_3d_to_2d(points):
    mk3d_cam = CAM_EXT[:3, :3] @ points.T + np.expand_dims(CAM_EXT[:3, 3], axis=1)
    uvw = CAM_INS.dot(mk3d_cam)
    uvw /= uvw[2]
    uvs = uvw[:2].T
    return uvs


rgb_files = sorted(os.listdir(rgb_folder))
mat_files = sorted(os.listdir(mat_folder))

if len(rgb_files) != len(mat_files):
    print("number of rgb != number of mat")
    exit()

for rgb_file, mat_file in zip(rgb_files, mat_files):
    timestamp_rgb = os.path.splitext(rgb_file)[0]
    timestamp_mat = os.path.splitext(mat_file)[0]

    if timestamp_rgb != timestamp_mat:
        print(f"{timestamp_rgb} - {timestamp_mat}")
        continue

    mat_data = scipy.io.loadmat(os.path.join(mat_folder, mat_file))
    RawPoints = mat_data['RawPoints'][:, :3]
    print(RawPoints)

    transformed_data = project_3d_to_2d(RawPoints)
    print(transformed_data.shape)

    inside_image_mask = (transformed_data[:, 0] > 0) & (transformed_data[:, 0] < image_width) & (
                transformed_data[:, 1] > 0) & (
                                transformed_data[:, 1] < image_height)
    transformed_data = transformed_data[inside_image_mask]

    rgb_image = Image.open(os.path.join(rgb_folder, rgb_file))

    plt.imshow(rgb_image)
    plt.scatter(transformed_data[:, 0], transformed_data[:, 1], s=1, cmap='viridis')
    plt.title(f"{timestamp_rgb}")
    plt.colorbar()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, f"{timestamp_rgb}.png")
    plt.savefig(output_path)
    plt.close()



def create_video_from_pngs(folder_path, output_video_path):
    images = [img for img in os.listdir(folder_path) if img.endswith(".png")]
    images.sort()

    img = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, layers = img.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_path, fourcc, 12.0, (width, height))

    for image in images:
        img_path = os.path.join(folder_path, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()


folder_path = 'E:/test/test/2024-01-19-21-14-10/test/'
output_video_path = 'E:/test/test/2024-01-19-21-14-10/point_cloud.mp4'

create_video_from_pngs(folder_path, output_video_path)
