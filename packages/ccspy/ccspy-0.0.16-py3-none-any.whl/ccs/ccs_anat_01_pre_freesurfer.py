#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ccspy_anat_01_pre_freesurfer.py
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/15 9:59   dzjin      1.0         None
"""

import os
import ccspy.utils.run_command_util as run_command
import logging
logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def run(CCS_DIR, SUBJECTS_DIR, subject):
    """
    run ccspy anat 01 pre freesurfer
    :param CCS_DIR:
    :param SUBJECTS_DIR:
    :param subject:
    :return:
    """
    logger = logging.getLogger(__name__)

    anat_dir = os.path.join(CCS_DIR, subject, 'anat')

    if CCS_DIR is None or SUBJECTS_DIR is None or subject is None:
        logger.error("Usage: {} {} CCS_DIR SUBJECTS_DIR subject".format(__file__, __name__))
        return

    T1image = os.path.join(CCS_DIR, subject, "anat/T1.nii.gz")
    if not os.path.exists(T1image):
        logger.error("Couldn't find T1 image {} please check your data".format(T1image))

    command = "cd "+anat_dir
    if not run_command.run(command):
        logger.error("Cant not enter {}".format(anat_dir))
        return

    return_code = run_command.run(command, env=None)
    print("return code is {}".format(return_code))

