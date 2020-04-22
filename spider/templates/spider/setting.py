# -*- coding: utf-8 -*-
"""爬虫配置文件"""
import sys
import os

# MYSQL
MYSQL_IP = ""
MYSQL_PORT = 3306
MYSQL_DB = ""
MYSQL_USER_NAME = ""
MYSQL_USER_PASS = ""

# REDIS
# IP:PORT 多个逗号分隔
REDISDB_IP_PORTS = "xxx:6379"
REDISDB_USER_PASS = ""
# 默认 0 到 15 共16个数据库
REDISDB_DB = 0

# 爬虫相关
# COLLECTOR
COLLECTOR_SLEEP_TIME = 1
COLLECTOR_TASK_COUNT = 10

# PARSER
PARSER_COUNT = 1
PARSER_SLEEP_TIME = 0
PARSER_TASK_COUNT = 1
PARSER_MAX_RETRY_TIMES = 100
# 是否主动执行添加 设置为False 需要手动调用start_monitor_task，适用于多进程情况下
PARSER_AUTO_START_REQUESTS = True

# 重新尝试失败的requests 当requests重试次数超过允许的最大重试次数算失败
RETRY_FAILED_REQUESTS = False
# request 超时时间，超过这个时间重新做（不是网络请求的超时时间）单位秒
REQUEST_TIME_OUT = 600  # 10分钟
# 保存失败的request
SAVE_FAILED_REQUEST = True

# 下载缓存 利用redis缓存，由于内存小，所以仅供测试时使用
RESPONSE_CACHED_ENABLE = False  # 是否启用下载缓存 成本高的数据或容易变需求的数据，建议设置为True
RESPONSE_CACHED_EXPIRE_TIME = 3600  # 缓存时间 秒
RESPONSE_CACHED_USED = False  # 是否使用缓存 补才数据时可设置为True

WARNING_FAILED_COUNT = 1000  # 任务失败数 超过WARNING_FAILED_COUNT则报警

# 爬虫初始化工作
# redis 存放item与request的根目录
TABLE_FOLDER = ""
# 每次启动时需要删除的表
DELETE_TABS = []
# 爬虫做完request后是否自动结束或者等待任务
AUTO_STOP_WHEN_SPIDER_DONE = True
# 是否将item添加到 mysql 支持列表 指定添加的item 可模糊指定
ADD_ITEM_TO_MYSQL = True
# 是否将item添加到 redis 支持列表 指定添加的item 可模糊指定
ADD_ITEM_TO_REDIS = False

# 设置代理
PROXY_ENABLE = True

# 随机headers
RANDOM_HEADERS = True
# requests 使用session
USE_SESSION = False

# 过滤
ITEM_FILTER_ENABLE = False
REQUEST_FILTER_ENABLE = False

# 报警
DINGDING_WARNING_URL = ""
DINGDING_WARNING_PHONE = ""
LINGXI_TOKEN = ""

LOG_NAME = os.path.basename(os.getcwd())
LOG_PATH = "log/%s.log" % LOG_NAME  # log存储路径
LOG_LEVEL = "DEBUG"
LOG_IS_WRITE_TO_FILE = False
OTHERS_LOG_LEVAL = "ERROR"  # 第三方库的log等级

project_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(project_path)  # 切换工作路经
sys.path.insert(0, project_path)
print("当前工作路径为 " + os.getcwd())
