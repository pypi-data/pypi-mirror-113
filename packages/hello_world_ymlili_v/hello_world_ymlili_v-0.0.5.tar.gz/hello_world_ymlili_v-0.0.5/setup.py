# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 10:03 上午
# @Author  : lili4cityu
# @File    : setup.py


# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = '0.0.5'


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


def load_require():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return f.read().split('\n')


setup(name='hello_world_ymlili_v',
      version=VERSION,
      description='hello_world',
      long_description=readme(),
      # 程序的关键字列表（？）
      # keywords='hello_world',
      author='lili',
      author_email='lili@yimian.com.cn',
      # 需要处理的包目录，也可以直接写成 setuptools.find_packages()
      packages=['hello_world'],
      # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
      install_requires=load_require(),
      # 自动包含包内所有受版本控制的数据文件
      include_package_data=True,
      # classifiers 说明包的分类信息
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      # 安装环境的限制
      python_requires='>=3.6',
      # 动态发现服务和插件（？）
      entry_points={
          'console_scripts': ['fword=hello_world:hello_world'],
      },
      zip_safe=False)
