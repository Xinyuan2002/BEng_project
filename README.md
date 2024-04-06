# BEng_project

The unprocessed Radar & RGB-D data is available at:
link: https://pan.baidu.com/s/1muGqz3sHmNDJU_CWt2aHvA
code: f5g8

Vicon data is available at:
link: https://pan.baidu.com/s/1euV5gBUYhxw2kgCDZGINGQ
code: ahya

Processing Steps:
1. Spatial calibration of Vicon and RGB-D: calib_vicon_cam.py
2. Check the accuracy of spatial calibration: project_marker.py
3. Process MoCap (Motion Capture data collected by Vicon) with SOMA:
   3.1 Set up SOMA， follwing the link: https://github.com/nghorbani/soma.git
   3.2 Store the .c3d data from Vicon in: \soma-main\support_files\evaluation_mocaps\original\SOMA_manual_labeled\soma_subject1
   3.3 Store gender data in: \soma-main\support_files\evaluation_mocaps\original\SOMA_manual_labeled\soma_subject1\setting.json
   3.4 Store the vertex numbers of points collected by MoCap in: \soma-main\running_just_mosh\mosh_results\SOMA_manual_labeled\SOMA_manual_labeled_smplx.json
   3.5 Code for generating .pkl files: Place `solve_labeled_mocap.py` in the `\soma-main\src\tutorials\` directory and execute it.

4. Generate joints, betas, trans, pose_body, and root_orient:
   4.1 Set up SMPL-X， following the link: https://github.com/vchoutas/smplx.git
   4.2 Code: Place `parameter_gen.py` in the `\smplx-main\` directory and execute it.

5. Generate Mesh:
   5.1 Code: Place `obj_gen.py` in the `\smplx-main\` directory and execute it.

6. Temporal calibration of Vicon and RGB-D:
   6.1 Align the first frame: findFirstFrame.py
   6.2 Align the joints, betas, trans, pose_body, and root_orient with each frame of RGB-D: parameterCut.py

7. Visualization:
   7.1 Visualize Mesh: Use Blender software, import vis_obj.py to run
   7.2 Generate Video, visualize RBG, Depth, joints, raw data：video_gen.py

The processed data is available at:
link: https://pan.baidu.com/s/141DZK7DxPUk9ByLgurkBMw
code: izhp
