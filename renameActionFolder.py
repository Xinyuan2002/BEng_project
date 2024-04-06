import os
import shutil

folder_path = 'E:/radar_DATA/5'
folders = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

folders.sort(key=lambda x: os.path.getmtime(x))

for i, folder in enumerate(folders, start=1):
    new_name = os.path.join(folder_path, str(i))
    shutil.move(folder, new_name)
    if i == 50:
        break

