from moshpp.mosh_head import MoSh
import numpy as np
import trimesh
from body_visualizer.tools.vis_tools import colors
from body_visualizer.mesh.sphere import points_to_spheres
from body_visualizer.tools.vis_tools import show_image

from human_body_prior.body_model.body_model import BodyModel
import torch
from human_body_prior.tools.omni_tools import copy2cpu as c2c 
import os.path as osp
import os
import json
import pickle
import torch
import smplx
import pickle
import re


os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

from smplx.lbs import (
   lbs, vertices2landmarks, find_dynamic_lmk_idx_and_bcoords, blend_shapes)
from smplx.utils import rot_mat_to_euler, Tensor


class SMPLX(BodyModel):
    def __init__(self, num_betas=16, **kwargs):
        super().__init__(bm_fname=SMPLX_MODEL_NEUTRAL_PATH, num_betas=16, num_expressions=0, **kwargs)
        self.faces = self.f

    def forward(self, pose_body, betas, use_rodrigues=True):
        device = pose_body.device
        for name in ['init_pose_hand', 'init_pose_jaw','init_pose_eye', 'init_v_template', 'init_expression',
                    'shapedirs', 'exprdirs', 'posedirs', 'J_regressor', 'kintree_table', 'weights', ]:
            _tensor = getattr(self, name)
            # if name == 'posedirs':
            #     print(f"Name: {name}, tensor: {_tensor}, tensor shape: {_tensor.shape}")
            setattr(self, name, _tensor.to(device))


        batch_size = pose_body.shape[0]
        trans = pose_body[:, :3]
        pose_hand = self.init_pose_hand.expand(batch_size, -1)
        pose_jaw = self.init_pose_jaw.expand(batch_size, -1)
        pose_eye = self.init_pose_eye.expand(batch_size, -1)
        v_template = self.init_v_template.expand(batch_size, -1, -1)
        expression = self.init_expression.expand(batch_size, -1)

        init_pose = torch.cat([pose_jaw, pose_eye, pose_hand], dim=-1)
        # if not use_rodrigues:
        #     init_pose = rodrigues_2_rot_mat(init_pose)
        print(f"init_pose shape: {init_pose.shape}")
        full_pose = torch.cat([pose_body[:, 3:], init_pose], dim=-1)
        # full_pose = torch.cat([pose_body[:, :], init_pose], dim=-1)
        print(f"full_pose shape: {full_pose.shape}")
        shape_components = torch.cat([betas, expression], dim=-1)
        shapedirs = torch.cat([self.shapedirs, self.exprdirs], dim=-1)

        verts, joints = lbs(betas=shape_components, pose=full_pose, v_template=v_template,
                        shapedirs=shapedirs, posedirs=self.posedirs, J_regressor=self.J_regressor,
                        parents=self.kintree_table[0].long(), lbs_weights=self.weights, pose2rot=use_rodrigues)

        joints = joints + trans.unsqueeze(dim=1)
        verts = verts + trans.unsqueeze(dim=1)
        return dict(vertices=verts, joints=joints)


def load_pickle_file(file_path):
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data

file_path = "E:/BEng_Project/parameters/p13-parameter/indix.pkl"
vertex_frames = load_pickle_file(file_path)
print(f'vertex_frames are {vertex_frames}')

input_folder = 'E:/BEng_Project/parameters/p13/'
output_folder = 'E:BEng_Project/parameters/p13-obj/'
soma_work_base_dir = 'E:/BEng_Project/soma-main'

os.makedirs(output_folder, exist_ok=True)

def save_tensor_to_json(joint, beta, tran, pose, root_orient, filename):
            # Convert PyTorch tensor to NumPy array and then to nested list
            tensor_list1 = joint.detach().cpu().numpy().tolist()
            tensor_list2 = beta.detach().cpu().numpy().tolist()
            tensor_list3 = tran.detach().cpu().numpy().tolist()
            tensor_list4 = pose.detach().cpu().numpy().tolist()
            tensor_list5 = root_orient.detach().cpu().numpy().tolist()
             
            # Create a dictionary with the "joints" key
            data_dict = {"joints": tensor_list1, "betas": tensor_list2, "trans": tensor_list3, "pose_body": tensor_list4, "root_orient": tensor_list5}

            # Save the dictionary to a JSON file
            with open(filename, 'w') as json_file:
                json.dump(data_dict, json_file)

def extract_number(string):
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    else:
        return None
    
for filename in os.listdir(input_folder):
    if filename.endswith('.pkl'):
        input_filepath = os.path.join(input_folder, filename)

        print(input_filepath)
        mosh_result = MoSh.load_as_amass_npz(input_filepath, include_markers=True)
        print({k:v if isinstance(v, str) or isinstance(v,float) or isinstance(v,int) else v.shape for k,v in mosh_result.items() if not isinstance(v, list) and not isinstance(v,dict)})

        time_length = len(mosh_result['trans'])
        mosh_result['betas'] = np.repeat(mosh_result['betas'][None], repeats=time_length, axis=0)

        subject_gender = mosh_result['gender']
        surface_model_type = mosh_result['surface_model_type']
        print(f'subject_gender: {subject_gender}, surface_model_type: {surface_model_type}, time_length: {time_length}')
        print(mosh_result['trans'])

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        bm_fname = osp.join(soma_work_base_dir, f'support_files/{surface_model_type}/{subject_gender}/model.npz')

        num_betas = mosh_result['num_betas'] # number of body parameters

        bm = BodyModel(bm_fname=bm_fname, num_betas=num_betas).to(device)
        faces = c2c(bm.f)
        print(faces)
        print(bm_fname)

        body_parms = {k:torch.Tensor(v).to(device) for k,v in mosh_result.items() if k in ['pose_body', 'betas', 'pose_hand']}
        # print({k:v.shape for k,v in body_parms.items()})
        print(mosh_result['betas'])
        print(mosh_result['pose_body'])
        # print(mosh_result['pose_hand'])
        # print(mosh_result.keys())
        # print(mosh_result['pose_body'][0])
        # print(mosh_result['poses'][0])
        # print(mosh_result['latent_labels'])

        SMPLX_MODEL_NEUTRAL_PATH = bm_fname
        betas = torch.tensor(mosh_result['betas']).to(device) 
        pose_body = torch.tensor(mosh_result['pose_body']).to(device) 
        trans = torch.tensor(mosh_result['trans']).to(device)
        root_orient = torch.tensor(mosh_result['root_orient']).to(device)
        pose_body = torch.cat([trans, root_orient, pose_body], dim=1)
        print(pose_body.shape)

        output = SMPLX(bm).forward(pose_body, betas, use_rodrigues=True)

        vertices = output['vertices']

        print(f"faces shape : {faces.shape}")
        print(vertices.shape)


        action = extract_number(os.path.splitext(filename)[0])
        output_f = os.path.join(output_folder, str(action))
        os.makedirs(output_f, exist_ok=True)

        data_dict = {
            'vertices': vertices, 
            'faces': faces,
        }

        for i in vertex_frames[int(action)-2]:
            vertices = data_dict['vertices'][i].numpy()
            faces = data_dict['faces']

            output_filepath = os.path.join(output_f, f'{i}.obj')

            with open(output_filepath, 'w') as obj_file:
                for vertex in vertices:
                    formatted_vertex = [f"{coord:.6f}" for coord in vertex]
                    obj_file.write(f"v {' '.join(formatted_vertex)}\n")

                for f in range(faces.shape[0] - 1):
                    obj_file.write(f"f {faces[f][0]} {faces[f][1]} {faces[f][2]}\n")

                obj_file.write(f"f {faces[-1][0]} {faces[-1][1]} {faces[-1][2]}")