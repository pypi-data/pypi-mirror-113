#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setup.py   
@Author  :   dzjin
@Contact :   dzjin5678@163.com
@License :   Nothing


@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/1 16:25   dzjin      1.0         None
"""

import setuptools

setuptools.setup(
    name="ccspy",  # Replace with your own username
    version="0.0.16",
    author="dzjin",
    author_email="dzjin5678@163.com",
    description="A CCS PACKAGE",
    long_description="A CCS PACKAGE",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    data_files=[('', ['README.md'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': [
            'ccspy_anat=ccspy.ccspy_anat:main',
            'ccspy_anat_01_pre_freesurfer=ccspy.ccspy_anat_01_pre_freesurfer:main',
            'ccspy_anat_02_freesurfer=ccspy.ccspy_anat_02_freesurfer:main',
            'ccspy_anat_03_postfs=ccspy.ccspy_anat_03_postfs:main',
            'ccspy_say_hello=ccspy.say_hello:main'
        ],
    },
    install_requires=[
            'docopt',
            'antspyx',
    ],
    include_package_data=True,
    python_requires='>=3.0',
)
