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

import os
import sys
import subprocess
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s')


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

    if type(command) is list:
        command = ' '.join(command)
    logger.info("[Running command]# "+command)

    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=merged_env)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')

    if len(out) > 0:
        logger.info(out)
    if len(err) > 0:
        logger.error(err)

    if p.returncode:
        # 指令运行出错，终止程序的执行
        logger.error('command: {} , Failed with returncode {}'.format(command, p.returncode))
        sys.exit()
    else:
        # 程序运行正常，正常返回
        return
