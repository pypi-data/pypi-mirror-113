#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The first step of this script is to run on bash will move to python eventually
Usage:
  ccspy_anat_03_postfs [options]

Options:
  --CCS_DIR PATH     The directory for CCS
  --SUBJECTS_DIR PATH     The directory for SUBJECTS
  --subject PATH       The subject's id
"""

from docopt import docopt
import os
import logging
import ccspy.utils.run_command_util as run_command
import ccspy.utils.logging_config_util as logging_config_util
import ccspy.utils.file_util as file_util


def postfs(CCS_DIR, SUBJECTS_DIR, subject, logger):

    anat_dir = os.path.join(CCS_DIR, subject, 'anat')
    reg_dir = os.path.join(anat_dir, 'reg')
    seg_dir = os.path.join(anat_dir, 'segment')

    file_util.make_dir(reg_dir)
    file_util.make_dir(seg_dir)

    # generate copy brainmask

    # copy orig.mgz
    if not os.path.exists(os.path.join(anat_dir, 'T1_crop_sanlm_fs_rpi.nii.gz')):
        command = ['mri_convert', '-it', 'mgz', os.path.join(SUBJECTS_DIR, subject, 'mri/orig.mgz'),
                   '-ot', 'nii', os.path.join(anat_dir, 'T1_crop_sanlm_fs.nii.gz')]
        run_command.run(command)

    if not os.path.exists(os.path.join(seg_dir, 'brainmask.nii.gz')):
        command = ['mri_convert', '-it', 'mgz', os.path.join(SUBJECTS_DIR, subject, 'mri/brainmask.mgz'),
                   '-ot', 'nii', os.path.join(seg_dir, 'brainmask.nii.gz')]
        run_command.run(command)

    # prepare anatomical images
    file_util.remove_file(os.path.join(reg_dir, 'highres_head.nii.gz'))

    command = ['mv', os.path.join(anat_dir, 'T1_crop_sanlm_fs.nii.gz'),
               os.path.join(reg_dir, 'highres_head.nii.gz')]
    run_command.run(command)

    # clean voxels manually edited in freesurfer (assigned value 1)
    command = ['fslmaths', os.path.join(seg_dir, 'brainmask.nii.gz'),
               '-thr', '2', os.path.join(seg_dir, 'brainmask.nii.gz')]
    run_command.run(command)

    command = ['fslmaths', os.path.join(reg_dir, 'highres_head.nii.gz'),
               '-mas', os.path.join(seg_dir, 'brainmask.nii.gz'),
               os.path.join(reg_dir, 'highres.nii.gz')]
    run_command.run(command)

    # command = ['cd', reg_dir]
    # run_command.run(command)
    os.chdir(reg_dir)

    # 1. copy standard (we provide two reg pipelines: FSL and Freesurfer,
    # the latter was done in recon-all automatically)
    out = run_command.run("echo ${FSLDIR}")
    out = out.replace('\n', '').replace('\r', '')

    standard_head = os.path.join(out, 'data/standard/MNI152_T1_2mm.nii.gz')
    standard = os.path.join(out, 'data/standard/MNI152_T1_2mm_brain.nii.gz')
    standard_mask = os.path.join(out, 'data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz')

    # command = ['standard_head=${FSLDIR}/data/standard/MNI152_T1_2mm.nii.gz']
    # run_command.run(command)
    #
    # run_command.run("echo ${standard_head}")
    #
    # command = ['standard=${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz']
    # run_command.run(command)
    #
    # command = ['standard_mask=${FSLDIR}/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz']
    # run_command.run(command)

    # 2. FLIRT T1->STANDARD
    logger.info("########## performing FLIRT T1 -> STANDARD ##########")
    command = ['fslreorient2std', 'highres.nii.gz', 'highres_rpi.nii.gz']
    run_command.run(command)

    # not used, just test for future use
    command = ['fslreorient2std', 'highres_head.nii.gz', 'highres_head_rpi.nii.gz']
    run_command.run(command)

    command = ['flirt', '-ref', standard, '-in', 'highres_rpi', '-out', 'highres_rpi2standard',
               '-omat', 'highres_rpi2standard.mat', '-cost', 'corratio', '-searchcost',
               'corratio', '-dof', '12', '-interp', 'trilinear']
    run_command.run(command)

    # 3. create mat file for conversion from standard to high res
    command = ['fslreorient2std', 'highres.nii.gz', '>', 'reorient2rpi.mat']
    run_command.run(command)

    command = ['convert_xfm', '-omat', 'highres2standard.mat', '-concat',
               'highres_rpi2standard.mat', 'reorient2rpi.mat']
    run_command.run(command)

    command = ['convert_xfm', '-inverse', '-omat', 'standard2highres.mat', 'highres2standard.mat']
    run_command.run(command)

    # 3. FNIRT
    logger.info("########## performing nolinear registration ... ##########")
    command = ['fnirt', '--in=highres_head', '--aff=highres2standard.mat',
               '--cout=highres2standard_warp', '--iout=fnirt_highres2standard',
               '--jout=highres2standard_jac', '--config=T1_2_MNI152_2mm',
               '--ref='+standard_head, '--refmask='+standard_mask,
               '--warpres=10,10,10', '>', 'warnings.fnirt']
    run_command.run(command)

    path = os.path.join(reg_dir, 'warnings.fnirt')
    if os.path.getsize(path) > 0:

        command = ['mv', 'fnirt_highres2standard.nii.gz', 'fnirt_highres2standard_wres10.nii.gz']
        run_command.run(command)

        command = ['fnirt', '--in=highres_head', '--aff=highres2standard.mat',
                   '--cout=highres2standard_warp', '--iout=fnirt_highres2standard',
                   '--jout=highres2standard_jac', '--config=T1_2_MNI152_2mm',
                   '--ref='+standard_head, '--refmask='+standard_mask,
                   '--warpres=20,20,20']
        run_command.run(command)

    else:
        file_util.remove_file(os.path.join(reg_dir, "warnings.fnirt"))

    # command = ['cd', '${cwd}']
    # run_command.run(command)
    os.chdir('/')


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

    postfs(CCS_DIR, SUBJECTS_DIR, subject, logger)

