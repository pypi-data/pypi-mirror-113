#!/usr/local/bin/ python3
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='nonebot_plugin_fr24',
    version='0.2.2',
    author='IronW',
    author_email='jhhh5hj@hotmail.com',
    url='https://github.com/IronWolf-K/nonebot_plugin_fr24',
    description=u'nonebot2航班查询',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['brotlipy']
)