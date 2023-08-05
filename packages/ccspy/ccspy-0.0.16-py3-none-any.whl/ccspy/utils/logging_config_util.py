#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   logging_config_util.py   
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/18 16:28   dzjin      1.0         None
"""

import os
import json
import logging.config


def config():
    path = os.path.join(os.path.dirname(__file__), "logging_config.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            logging.config.dictConfig(json.load(f))
    else:
        logging.basicConfig(level=logging.INFO)
