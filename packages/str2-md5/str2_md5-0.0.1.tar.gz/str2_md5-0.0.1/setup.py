# -*- coding: UTF-8 -*-
# __name__ = setup.py

import os
import setuptools


setuptools.setup(
    name="str2_md5",  # 库名，需要在pypi中唯一
    version="0.0.1",  # 版本号
    author="Jacks",  # 作者
    author_email="fsym5320@163.com",  # 作者邮箱（方便使用者发现问题后联系我们）
    description="Hello pip",  # 简介
    long_description='str转换大写MD5格式方法',  # 详细描述（一般会写在README.md中）
    long_description_content_type="text/markdown",  # README.md中描述的语法（一般为markdown）
    url="https://github.com/fsym5320",  # 库/项目主页，一般我们把项目托管在GitHub，放该项目的GitHub地址即可
    packages=setuptools.find_packages(),  # 默认值即可，这个是方便以后我们给库拓展新功能的
    classifiers=[  # 指定该库依赖的Python版本、license、操作系统之类的
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.6',
)