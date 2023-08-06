#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='cv2box',  # 项目的名称,pip3 install get-time
    version='0.0.1',  # 项目版本
    author='ykk',  # 项目作者
    author_email='ykk648@gmail.com',  # 作者email
    url='https://github.com/ykk648/cv2box',  # 项目代码仓库
    description='cv toolbox',  # 项目描述
    packages=find_packages(),  # 包名
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
