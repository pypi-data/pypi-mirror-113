#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   run_command_util.py
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/15 10:05   dzjin      1.0         None
"""

import time
import os
import subprocess
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
import sys


def run(command, env=None):
    """
    运行命令行命令
    :param command: 命令
    :param env: 字符串环境
    :return: 返回码
    """

    logger = logging.getLogger(__name__)

    merged_env = os.environ
    if env:
        merged_env.update(env)

    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=merged_env)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')

    if p.returncode:
        logger.error('cmd: {} \n Failed with returncode {}'.format(command, p.returncode))
    if len(out) > 0:
        logger.info(out)
    if len(err) > 0:
        logger.warning(err)

    return p.returncode
