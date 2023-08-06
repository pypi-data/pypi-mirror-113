#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name='ascendfly',
    version='0.1',
    description='Ascend inference framework',
    keywords='ascend detection and classification',
    packages=find_packages(exclude=('configs', 'tools', 'cv2', 'tests', 'docs')),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://gitee.com/ascend-fae/ascendfly',
    author='zhengguojian',
    author_email='kfengzheng@163.com',
    install_requires=['numpy>=1.14', 'av>=8.0.2', 'objgraph>=3.5.0', 'opencv-python>=3.4.2', 'prettytable>=2.1.0'],
    zip_safe=False)
