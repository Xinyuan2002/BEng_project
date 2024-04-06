import cv2
import os

def create_video(input_folder, output_video_file, frame_rate=12):

    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(os.path.splitext(x)[0]))  # 假设文件名为数字

    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video_file, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(input_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def convert_depth_images_to_video(input_folder, output_video_path, frame_rate):
    depth_image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    depth_image_files = sorted(depth_image_files, key=lambda x: int(os.path.splitext(x)[0]))

    first_image = cv2.imread(os.path.join(input_folder, depth_image_files[0]), cv2.IMREAD_UNCHANGED)
    height, width = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height), isColor=True)

    for depth_image_file in depth_image_files:
        depth_image_path = os.path.join(input_folder, depth_image_file)

        depth_image = cv2.imread(depth_image_path, cv2.IMREAD_UNCHANGED)

        colored_depth_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        out.write(colored_depth_image)

    out.release()


input_folder = "E:/test/test/2024-01-19-21-14-10/test"
output_video_file = "E:/test/point_cloud.mp4"
frame_rate = 12

# convert_depth_images_to_video(input_folder, output_video_file, frame_rate)

create_video(input_folder, output_video_file)
