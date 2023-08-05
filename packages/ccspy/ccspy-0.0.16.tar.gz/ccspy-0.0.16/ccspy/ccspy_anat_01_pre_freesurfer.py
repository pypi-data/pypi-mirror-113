#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The first step of this script is to run on bash will move to python eventually
Usage:
  ccspy_anat_01_pre_freesurfer [options]

Options:
  --CCS_DIR PATH     The directory for CCS
  --SUBJECTS_DIR PATH     The directory for SUBJECTS
  --subject PATH       The subject's id
"""

import os
import logging
import ants
from docopt import docopt
import ccspy.utils.run_command_util as run_command_util
import ccspy.utils.logging_config_util as logging_config_util


def pre_freesurfer(CCS_DIR, subject, logger):

    anat_dir = os.path.join(CCS_DIR, subject, 'anat')

    path = os.path.join(CCS_DIR, subject, "anat/T1.nii.gz")
    if not os.path.exists(path):
        logger.error("\nCouldn't find T1 image {} please check your data".format(path))
        return

    # 1.crop the image
    if not os.path.exists(os.path.join(anat_dir, "T1_crop.nii.gz")):
        logger.info("Croping image")
        command = ["robustfov", "-i",
                   os.path.join(anat_dir, "T1.nii.gz"), "-r", os.path.join(anat_dir, "T1_crop.nii.gz")]
        run_command_util.run(command, env=None)

    # 2.using SANLM to denoise image
    if not os.path.exists(os.path.join(anat_dir, "T1_crop_sanlm.nii.gz")):

        logger.info("desonising image")

        # use python ants package antspyx replace matlab denoise
        input_image = ants.image_read(os.path.join(anat_dir, 'T1_crop.nii.gz'))
        output_image = ants.denoise_image(input_image, v=1)
        ants.image_write(output_image, os.path.join(anat_dir, 'T1_crop_sanlm.nii.gz'))

        # path = os.path.join(anat_dir, "denoise")
        # if not os.path.exists(path):
        #     os.makedirs(path)
        #
        # command = ['mri_convert', '-i', os.path.join(anat_dir, 'T1_crop.nii.gz'),
        #            '-o', os.path.join(anat_dir, 'denoise', 'T1_crop.nii')]
        # run_command_util.run(command)

        # command = ['matlab', '-nodesktop', '-nosplash', '-nojvm', '-r',
        #            "\"data='{}/denoise/T1_crop.nii';cat_vol_sanlm(struct('data',data));quit\"".format(anat_dir)]
        # run_command_util.run(command)
        #
        # command = ['mri_convert', '-i', os.path.join(anat_dir, 'denoise', 'sanlm_T1_crop.nii'),
        #            '-o', os.path.join(anat_dir, 'T1_crop_sanlm.nii.gz')]
        # run_command_util.run(command)

        # remove denoise dirs
        # os.removedirs(os.path.join(anat_dir, 'denoise'))

    # 3.deepbet to making brain mask
    if not os.path.exists(os.path.join(anat_dir, 'T1_crop_sanlm_pre_mask.nii.gz')):
        logger.info("making mask by deep_bet")

        command = ['docker', 'run', '-v', '{}:/data'.format(anat_dir), '-v', '${CCS_APP}/Models:/Models',
                   '-v', '{}:/output'.format(anat_dir), '--privileged=true',
                   'sandywangrest/deepbet', 'muSkullStrip.py',
                   '-in', '/data/T1_crop_sanlm.nii.gz', '-model', '/Models/model-04-epoch',
                   '-out', '/output']
        run_command_util.run(command)

        path = os.path.join(anat_dir, "qc")
        if not os.path.exists(path):
            os.makedirs(path)

        command = ['overlay', '1', '1', '{}/T1_crop_sanlm.nii.gz'.format(anat_dir),
                   '-a', '{}/T1_crop_sanlm_pre_mask.nii.gz'.format(anat_dir),
                   '1', '1', '{}/qc/T1_rendermask.nii.gz'.format(anat_dir)]
        run_command_util.run(command)

        command = ['slicer', '{}/qc/T1_rendermask.nii.gz'.format(anat_dir),
                   '-S', '10', '1200', '{}/qc/mask.png'.format(anat_dir)]
        run_command_util.run(command)

        title = subject + '.anat.UNet.skullstrip'
        command = ['convert', '-font', 'helvetica', '-fill', 'white', '-pointsize', '36',
                   '-draw', "\"text 30,50 '{}'\"".format(title),
                   "{}/qc/mask.png".format(anat_dir), "{}/qc/mask.png".format(anat_dir)]
        run_command_util.run(command)

        os.remove(os.path.join(anat_dir, "qc", "T1_rendermask.nii.gz"))


def main():

    arguments = docopt(__doc__)
    CCS_DIR = arguments['--CCS_DIR']
    # SUBJECTS_DIR = arguments['--SUBJECTS_DIR']
    subject = arguments['--subject']

    logging_config_util.config()
    logger = logging.getLogger(__name__)

    logger.info("CCS_DIR: " + CCS_DIR)
    # logger.info("SUBJECTS_DIR: " + SUBJECTS_DIR)
    logger.info("subject: " + subject)

    if CCS_DIR is None or subject is None:
        logger.error("\nUsage: {} {} CCS_DIR SUBJECTS_DIR subject".format(__file__, __name__))
        return

    pre_freesurfer(CCS_DIR, subject, logger)








