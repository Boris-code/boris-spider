# -*- coding: utf-8 -*-
"""
Created on {DATE}
---------
@summary: 爬虫入口
---------
@author: {USER}
"""

from spider.utils.custom_argparse import ArgumentParser

# 需配置
from parsers import *


def crawl_xxx():
    """
    普通爬虫
    """
    spider = xxx.XXXSpider(table_folder="xxx:xxx")
    spider.start()


def crawl_xxx(args):
    """
    批次爬虫
    @param args: 1 / 2 / init
    """
    spider = xxx_spider.XXXSpider(
        task_table="",  # mysql中的任务表
        batch_record_table="",  # mysql中的批次记录表
        batch_name="xxx(月增)",  # 批次名字
        batch_interval=7,  # 批次时间 天为单位 若为小时 可写 1 / 24
        task_keys=["id", "xxx"],  # 需要获取任务表里的字段名，可添加多个
        table_folder="xxx:xxxx",  # redis中存放request等信息的根key
        task_state="state",  # mysql中任务状态字段
        # min_task_count=1, # 任务池中最小任务数
        # task_limit=1, # 每次取的任务数
        # related_table_folder=None,  # 相关爬虫的table_folder
        # related_batch_record=None  # 相关爬虫的批次记录表
    )

    if args == 1:
        spider.start_monitor_task()
    elif args == 2:
        spider.start()
    elif args == "init":
        spider.init_task()


def upload_item():
    from spider.base.upload_item import upload_item

    upload_item.run()


if __name__ == "__main__":
    parser = ArgumentParser(description="xxx爬虫")

    parser.add_argument(
        "--upload_item", action="store_true", help="上传item", function=upload_item
    )

    parser.add_argument(
        "--crawl_xxx", action="store_true", help="xxx", function=crawl_xxx
    )
    parser.add_argument(
        "--crawl_xxx", type=int, nargs=1, help="xxx(1|2）", function=crawl_xxx
    )

    parser.start()
