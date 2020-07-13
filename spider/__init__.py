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

current_path = os.getcwd()
sys.path.insert(0, os.getcwd().replace("/items", ""))
sys.path.insert(0, os.getcwd().replace("/parsers", ""))

__all__ = [
    "SingleSpider",
    "Spider",
    "BatchSpider",
    "Request",
    "Response",
    "Item",
    "UpdateItem",
    "ArgumentParser",
]

from spider.core.spiders import Spider, BatchSpider, SingleSpider
from spider.network.request import Request
from spider.network.response import Response
from spider.network.item import Item, UpdateItem
from spider.utils.custom_argparse import ArgumentParser
