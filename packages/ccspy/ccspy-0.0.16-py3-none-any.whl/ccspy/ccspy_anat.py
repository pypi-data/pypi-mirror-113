#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
The first step of this script is to run on bash will move to python eventually
Usage:
  ccspy_anat [options]

Options:
  --CCS_DIR PATH     The directory for CCS
  --SUBJECTS_DIR PATH     The directory for SUBJECTS
  --subject PATH       The subject's id
"""

import os
import logging
from docopt import docopt
import ccspy.utils.run_command_util as run_command_util
import ccspy.utils.logging_config_util as lcu
import ccspy.ccspy_anat_01_pre_freesurfer as ccs_anat_01
import ccspy.ccspy_anat_02_freesurfer as ccs_anat_02
import ccspy.ccspy_anat_03_postfs as ccs_anat_03


def main():

    arguments = docopt(__doc__)
    CCS_DIR = arguments['--CCS_DIR']
    SUBJECTS_DIR = arguments['--SUBJECTS_DIR']
    subject = arguments['--subject']

    lcu.config()
    logger = logging.getLogger(__name__)

    logger.info("CCS_DIR: " + CCS_DIR)
    logger.info("SUBJECTS_DIR: " + SUBJECTS_DIR)
    logger.info("subject: " + subject)

    if CCS_DIR is None or SUBJECTS_DIR is None or subject is None:
        logger.error("\nUsage: {} {} CCS_DIR SUBJECTS_DIR subject".format(__file__, __name__))
        return

    ccs_anat_01.pre_freesurfer(CCS_DIR, subject, logger)
    ccs_anat_02.freesurfer(CCS_DIR, SUBJECTS_DIR, subject, logger)
    ccs_anat_03.postfs(CCS_DIR, SUBJECTS_DIR, subject, logger)


if __name__ == "__main__":
    main()

