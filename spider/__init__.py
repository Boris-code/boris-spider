# -*- coding: utf-8 -*-
"""
Created on 2020/4/21 10:41 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
"""
import os, sys
import re

sys.path.insert(0, re.sub(r"([\\/]items)|([\\/]parsers)", "", os.getcwd()))

__all__ = [
    "SingleSpider",
    "Spider",
    "BatchSpider",
    "BaseParse",
    "BatchParser",
    "Request",
    "Response",
    "Item",
    "UpdateItem",
    "ArgumentParser",
]

from spider.core.spiders import Spider, BatchSpider, SingleSpider
from spider.core.base_parser import BaseParse, BatchParser
from spider.network.request import Request
from spider.network.response import Response
from spider.network.item import Item, UpdateItem
from spider.utils.custom_argparse import ArgumentParser
