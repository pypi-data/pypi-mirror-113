#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time : 2021/7/12 上午10:01
# @Author : wangchong
# @Email: chongwangcc@gmail.com
# @Software: PyCharm
'''

from setuptools import setup
with open("README.rst", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setup(
    name='weightunit',
    version='0.0.4',
    author='chongwangcc',
    author_email='chongwangcc@gmail.com',
    url="https://github.com/chongwangcc/weightunit",
    description=u'提取淘宝title中的单位字符串，并且进行重量计算',
    long_description=long_description,
    # long_description_content_type="text/x-rst",
    packages=['weightunit', ],
    install_requires=[],
    entry_points={
    }
)
