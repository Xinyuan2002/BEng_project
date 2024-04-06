import json
import os
from datetime import datetime
import re
import pickle

# p13_start_frame = [41, 278, 321, 294, 289,
#                    403, 297, 408, 282, 303,
#                    318, 388, 360, 433, 802,
#                    394, 328, 358, 512, 515,
#                    395, 409, 342, 346, 344,
#                    345, 310, 366, 345, 263,
#                    202, 458, 399, 496, 624,
#                    466, 403, 438, 513, 383,
#                    666, 333, 405, 437, 435,
#                    368, 295, 347, 342, 461]

# p1_start_frame = [0, 106, 300, 120, 46, 
#                   59, 142, 267, 226, 164,
#                   93, 153, 190, 197, 140,
#                   200, 242, 208, 228, 572,
#                   165, 106, 121, 137, 162,
#                   154, 138, 167, 76, 138,
#                   36, 456, 517, 348, 334,
#                   227, 358, 176, 168, 324,
#                   386, 128, 178, 52, 87,
#                   101, 73, 318, 196, 71]

p5_start_frame = [196, 93, 300, 246, 334,
                  235, 298, 324, 284, 363,
                  419, 273, 458, 402, 427,
                  278, 308, 250, 258, 312,
                  218, 338, 288, 282, 240,
                  256, 255, 340, 178, 288,
                  336, 558, 470, 732, 544,
                  452, 319, 258, 352, 350,
                  288, 366, 328, 333, 332,
                  286, 245, 396, 408, 688]

def get_timestamps(folder_path):
    timestamps = set()
    for filename in os.listdir(folder_path):
        match = re.search(r'\d+', filename)
        if match:
            timestamps.add(match.group())
    return timestamps


def clean_folder(parent_folder):
    for folder in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder)
        if os.path.isdir(folder_path):
            depth_timestamps = get_timestamps(os.path.join(folder_path, 'depth'))
            mmwave_timestamps = get_timestamps(os.path.join(folder_path, 'mmwave'))
            rgb_timestamps = get_timestamps(os.path.join(folder_path, 'rgb'))

            common_timestamps = depth_timestamps & mmwave_timestamps & rgb_timestamps

            for subfolder in ['depth', 'mmwave', 'rgb']:
                subfolder_path = os.path.join(folder_path, subfolder)
                for filename in os.listdir(subfolder_path):
                    match = re.search(r'\d+', filename)
                    if match and match.group() not in common_timestamps:
                        os.remove(os.path.join(subfolder_path, filename))


vayyar_path = 'E:/radar_DATA/5'
json_file_path = 'E:/soma_parameter/p5'
png_folder_path = 'E:/radar_DATA/5'
output_json_path = 'E:/soma_parameter/p5_cut'

clean_folder(vayyar_path)


# #
# #
# for sub1dir in os.listdir(vayyar_path):
#     sub1dir_path = os.path.join(vayyar_path, sub1dir)

#     if os.path.isdir(sub1dir_path):
#         for sub2dir in os.listdir(sub1dir_path):
#             if(sub2dir == "body_mesh"):
#                 continue
#             sub2dir_path = os.path.join(sub1dir_path, sub2dir)

#             files = [f for f in os.listdir(sub2dir_path)]
#             min_number = min(int(f.split('.')[0][5:]) for f in files)

#             if files[0].endswith(".png"):
#                 suffix = ".png"
#             if files[0].endswith(".mat"):
#                 suffix = ".mat"

#             for file in files:
#                 old_path = os.path.join(sub2dir_path, file)
#                 number = int(file.split('.')[0][5:])

#                 new_filename = str(int((number - min_number) / (10 ** 7))) + suffix
#                 new_path = os.path.join(sub2dir_path, new_filename)
#                 os.rename(old_path, new_path)
#                 print(f"Renamed {file} to {new_filename}")

indixForAllActs = []
for i in range(1, 51):
    json_file = os.path.join(json_file_path, f'{i}.json')
    with open(json_file, 'r') as file:
        data = json.load(file)

    png_folder = os.path.join(png_folder_path, str(i), "rgb")

    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]
    def extract_number(filename):
        return int(filename.split('.')[0])

    png_files.sort(key=extract_number)
    
    indices = [int(os.path.splitext(f)[0]) + p5_start_frame[i-1] for f in png_files]
    print(f'indices for action {i} is :{indices}')
    indixForAllActs.append(indices)

    print(len(data['joints']))
    extracted_data = {'joints': [], 'betas': [], 'pose_body': [], 'trans': [], 'root_orient': []}
    for index in indices:
        extracted_data['joints'].append(data['joints'][index])
        extracted_data['betas'].append(data['betas'][index])
        extracted_data['pose_body'].append(data['pose_body'][index])
        extracted_data['trans'].append(data['trans'][index])
        extracted_data['root_orient'].append(data['root_orient'][index])

    output_json = os.path.join(output_json_path, f'{i}.json')
    with open(output_json, 'w') as outfile:
        json.dump(extracted_data, outfile)
    
with open('E:/soma_parameter/p5/indix.pkl', 'wb') as f:
    pickle.dump(indixForAllActs, f)

# with open('E:/soma_parameter/p13/indix.pkl', 'rb') as f:
#     loaded_list = pickle.load(f)

# print(loaded_list[1])