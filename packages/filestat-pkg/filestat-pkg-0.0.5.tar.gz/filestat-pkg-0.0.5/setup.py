#!/usr/bin/python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filestat-pkg",  # 名称为以后pip安装包的名字，后面最好加上用户名，避免名称冲突
    version="0.0.5",
    author="zdfzdf",
    author_email="2239432836@qq.com",
    description="Analyze the format of all files in the given path",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zdf123zdf/filestat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # exapmle
        'prettytable'
    ],
    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 filestat_pkg/filest.py 的main 函数
    entry_points={
        'console_scripts': [
            'filest = filestat_pkg.filest:main'
        ]
    },
    scripts=['filestat_pkg/filest.py']
)
