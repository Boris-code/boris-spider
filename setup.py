# -*- coding: utf-8 -*-
"""
Created on 2020/4/22 10:45 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
"""

from os.path import dirname, join
from sys import version_info

import setuptools

if version_info < (3, 6, 0):
    raise SystemExit("Sorry! spider requires python 3.6.0 or later.")

with open(join(dirname(__file__), "spider/VERSION"), "rb") as f:
    version = f.read().decode("ascii").strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()
packages.extend(
    [
        "spider.templates",
        "spider.templates.spider",
        "spider.templates.spider.parsers",
        "spider.templates.spider.items",
    ]
)

setuptools.setup(
    name="boris-spider",
    version=version,
    author="Boris",
    license="MIT",
    author_email="boris@bzkj.tech",
    description="A high-level Web Crawling and Web Scraping framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[  # 工具包的依赖包
        "better-exceptions==0.2.2",
        "DBUtils==1.3",
        "parsel==1.5.2",
        "PyExecJS==1.5.1",
        "PyMySQL==0.9.3",
        "redis==2.10.6",
        "requests>=2.22.0",
        "bs4==0.0.1",
        "ipython==7.14.0",
        "bitarray==1.5.3"
    ],
    entry_points={"console_scripts": ["spider = spider.commands.cmdline:execute"]},
    url="https://github.com/Boris-code/boris-spider.git",
    packages=packages,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
