#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   say_hello.py   
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/1 16:23   dzjin      1.0         None
"""

import os
import logging
import ccspy.utils.logging_config_util as lcu


def main():
    print("Hello ,This is my Python library.")
    # run_command.run('pwd')
    # run_command.run('cksdnvknfdvnfd')
    # print('1')
    # fun_test_return()
    # print('2')
    # fun_test_sys_exit()
    # print('3')

    test_logging_config()


# def fun_test_return():
#     print('fun_test_return')
#     return
#
#
# def fun_test_sys_exit():
#     print('fun_test_sys_exit')
#     sys.exit()


def test_logging_config():

    # logging.basicConfig(filename=os.path.join("d:\python", "out.log"), level=logging.DEBUG)

    lcu.config()
    logger = logging.getLogger(__name__)

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.error(__name__)
    logger.error(os.path.dirname(__file__))


if __name__ == '__main__':
    test_logging_config()

