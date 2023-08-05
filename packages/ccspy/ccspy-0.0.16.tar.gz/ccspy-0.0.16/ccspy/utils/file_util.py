#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   file_util.py
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/18 11:05   dzjin      1.0         None, add make_dir
2021-6-19 17:49   dzjin      1.0         None, add remove file(file and dir)
"""

import os
import sys
import logging


def make_dir(path, suppress_exists_error=False):
    """
    创建文件夹
    :param path: 待创建文件夹路径
    :param suppress_exists_error: 是否忽略FileExistsError
    :return:
    """
    logger = logging.getLogger(__name__)

    try:
        os.makedirs(path)
    except PermissionError:
        # 没有权限创建时，程序强制结束
        logger.error("You do not have permission to write to {}".format(path))
        sys.exit()
    except FileExistsError:
        if suppress_exists_error:
            logger.warning("{} already exists".format(path))
    except OSError:
        logger.error('Could not create directory {}'.format(path))
        sys.exit()


def remove_file(path):
    """
    删除文件或者文件夹
    :param path:
    :return:
    """
    logger = logging.getLogger(__name__)
    if os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            # 没有权限删除时，程序不强制结束
            logger.error("You do not have permission to remove {}".format(path))
        except OSError:
            logger.error('Could not remove file {}'.format(path))
            sys.exit()
