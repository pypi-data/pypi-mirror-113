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

from docopt import docopt
import os
import logging
import ccspy.utils.run_command_util as run_command_util
import ccspy.utils.logging_config_util as logging_config_util
import ccspy.utils.file_util as file_util


def freesurfer(CCS_DIR, SUBJECTS_DIR, subject, logger):
    anat_dir = os.path.join(CCS_DIR, subject, 'anat')

    path = os.path.join(anat_dir, "T1_crop_sanlm.nii.gz")
    if not os.path.exists(path):
        logger.error("\nCouldn't find T1_crop_sanlm.nii.gz image {} please check your data".format(path))
        return

    file_util.make_dir(os.path.join(SUBJECTS_DIR, subject, 'mri/orig'))

    # convert T1_crop_sanlm to 001.mgz
    command = ['mri_convert', '-i', os.path.join(anat_dir, 'T1_crop_sanlm.nii.gz'),
               '-o', os.path.join(SUBJECTS_DIR, subject, 'mri/orig/001.mgz')]
    run_command_util.run(command)

    # first stage of recall-all
    command = ['recon-all', '-s', subject, '-autorecon1', '-gcut', '-parallel']
    run_command_util.run(command)

    # convert brainmask
    logger.info("\n########## Changing orig brainmask by the deep_bet brainmask ##########")
    command = ['mri_convert', os.path.join(SUBJECTS_DIR, subject, 'mri/T1.mgz'),
               os.path.join(SUBJECTS_DIR, subject, 'mri/T1.nii.gz')]
    run_command_util.run(command)

    command = ['3dresample', '-master', os.path.join(SUBJECTS_DIR, subject, 'mri/T1.nii.gz'),
               '-inset', os.path.join(anat_dir, 'T1_crop_sanlm_pre_mask.nii.gz'),
               '-prefix', os.path.join(SUBJECTS_DIR, subject, 'mri/mask.nii.gz')]
    run_command_util.run(command)

    command = ['fslmaths', os.path.join(SUBJECTS_DIR, subject, 'mri/T1.nii.gz'),
               '-mas', os.path.join(SUBJECTS_DIR, subject, 'mri/mask.nii.gz'),
               os.path.join(SUBJECTS_DIR, subject, 'mri/brainmask.nii.gz')]
    run_command_util.run(command)

    command = ['mv', os.path.join(SUBJECTS_DIR, subject, 'mri/brainmask.mgz'),
               os.path.join(SUBJECTS_DIR, subject, 'mri/brainmask.fsinit.mgz')]
    run_command_util.run(command)

    command = ['mri_convert', '-i', os.path.join(SUBJECTS_DIR, subject, 'mri/brainmask.nii.gz'),
               '-o', os.path.join(SUBJECTS_DIR, subject, 'mri/brainmask.mgz')]
    run_command_util.run(command)

    # recon-all 2 3
    command = ['recon-all', '-s', subject, '-autorecon2', '-autorecon3', '-parallel']
    run_command_util.run(command)


def main():

    arguments = docopt(__doc__)
    CCS_DIR = arguments['--CCS_DIR']
    SUBJECTS_DIR = arguments['--SUBJECTS_DIR']
    subject = arguments['--subject']

    logging_config_util.config()
    logger = logging.getLogger(__name__)

    logger.info(CCS_DIR)
    logger.info(SUBJECTS_DIR)
    logger.info(subject)

    if CCS_DIR is None or SUBJECTS_DIR is None or subject is None:
        logger.error("\nUsage: {} {} CCS_DIR SUBJECTS_DIR subject".format(__file__, __name__))
        return

    freesurfer(CCS_DIR, SUBJECTS_DIR, subject, logger)
