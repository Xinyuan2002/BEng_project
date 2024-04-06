import os.path as osp
from glob import glob
import os
import numpy as np
from loguru import logger
import sys
sys.path.append("/BEng_Project/soma-main/src/")

from soma.amass.mosh_manual import mosh_manual

soma_work_base_dir = '/BEng_Project/soma-main/'
support_base_dir = osp.join(soma_work_base_dir, 'support_files')

mocap_base_dir = osp.join(support_base_dir, 'evaluation_mocaps/original-1')

work_base_dir = osp.join(soma_work_base_dir, 'running_just_mosh-1')

target_ds_names = ['SOMA_manual_labeled',]

for ds_name in target_ds_names:
    mocap_fnames = glob(osp.join(mocap_base_dir, ds_name,  '*/*.c3d'))

    logger.info(f'#mocaps found for {ds_name}: {len(mocap_fnames)}')

    mosh_manual(
        mocap_fnames,
        mosh_cfg={
            'moshpp.verbosity': 1, # set to 2 to visulaize the process in meshviewer
            'dirs.work_base_dir': osp.join(work_base_dir, 'mosh_results'),
            'dirs.support_base_dir': support_base_dir,
        },
        render_cfg={
            'dirs.work_base_dir': osp.join(work_base_dir, 'mp4_renders'),
            'render.render_engine': 'eevee',  # eevee / cycles,
            # 'render.render_engine': 'cycles',  # eevee / cycles,
            'render.show_markers': True,
            # 'render.save_final_blend_file': True
            'dirs.support_base_dir': support_base_dir,

        },
        parallel_cfg={
            'pool_size': 1,
            'max_num_jobs': 10,
            'randomly_run_jobs': False,
        }, 
        run_tasks=[
            'mosh',
            # 'render',
        ],
        fast_dev_run=True,
    )