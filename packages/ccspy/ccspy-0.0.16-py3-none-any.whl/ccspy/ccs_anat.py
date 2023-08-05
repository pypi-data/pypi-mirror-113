#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ccspy_anat.py
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/19 10:21   dzjin      1.0         None
"""

"""
The first step of this script is to run on bash will move to python eventually
Usage:
  ccs_anat_01_pre_freesurfer [options]

Options:
  --CCS_DIR PATH     The directory for CCS
  --SUBJECTS_DIR PATH     The directory for SUBJECTS
  --subject PATH       The subject's id
"""

import os
import logging
from docopt import docopt
import ccspy.utils.run_command_util as run_command_util
import ccspy.utils.logging_config_util as logging_config_util


def main():

    arguments = docopt(__doc__)
    CCS_DIR = arguments['--CCS_DIR']
    SUBJECTS_DIR = arguments['--SUBJECTS_DIR']
    subject = arguments['--subject']

    logging_config_util.config()
    logger = logging.getLogger(__name__)

    logger.info("CCS_DIR: " + CCS_DIR)
    logger.info("SUBJECTS_DIR: " + SUBJECTS_DIR)
    logger.info("subject: " + subject)

    if CCS_DIR is None or SUBJECTS_DIR is None or subject is None:
        logger.error("\nUsage: {} {} CCS_DIR SUBJECTS_DIR subject".format(__file__, __name__))
        return
