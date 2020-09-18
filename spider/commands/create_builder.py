# -*- coding: utf-8 -*-
"""
Created on 2018-08-28 17:38:43
---------
@summary: 模版生成器
---------
@author: Boris
@email:  boris_liu@foxmail.com
"""

import argparse
import getpass
import os
import re
import shutil
import sys
import time

import spider.setting as setting
import spider.utils.tools as tools
from spider.db.mysqldb import MysqlDB
from spider.utils.tools import key2underline, dumps_json


def deal_file_info(file):
    file = file.replace("{DATE}", tools.get_current_date())
    file = file.replace("{USER}", getpass.getuser())

    return file


class CreateItem:
    def __init__(self):
        self._db = MysqlDB()
        self._create_init = CreateInit()

    def select_columns(self, table_name):
        # sql = 'SHOW COLUMNS FROM ' + table_name
        sql = "SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, EXTRA, COLUMN_KEY, COLUMN_COMMENT FROM INFORMATION_SCHEMA.Columns WHERE table_name = '{}'".format(
            table_name
        )
        columns = self._db.find(sql)

        return columns

    def select_tables_name(self, tables_name):
        """
        @summary:
        ---------
        @param tables_name: 一类tables 如 qidian*
        ---------
        @result:
        """
        sql = (
            "select table_name from information_schema.tables where table_name like '%s'"
            % tables_name
        )
        tables_name = self._db.find(sql)

        return tables_name

    def convert_table_name_to_hump(self, table_name):
        """
        @summary: 格式化表明为驼峰格式
        ---------
        @param table:
        ---------
        @result:
        """
        table_hump_format = ""

        words = table_name.split("_")
        for word in words:
            table_hump_format += word.capitalize()  # 首字母大写

        return table_hump_format

    def get_item_template(self):
        templete_path = os.path.abspath(
            os.path.join(__file__, "../../templates/item_template.tmpl")
        )
        with open(templete_path, "r", encoding="utf-8") as file:
            item_template = file.read()

        return item_template

    def create_item(self, item_template, columns, table_name_hump_format, support_dict):
        # 组装 类名
        item_template = item_template.replace("${table_name}", table_name_hump_format)

        # 组装 属性
        propertys = ""
        for column in columns:
            column_name = column[0]
            column_type = column[1]
            is_nullable = column[2]
            column_default = column[3]
            column_extra = column[4]
            column_key = column[5]
            column_comment = column[6]

            try:
                value = (
                    "kwargs.get('{column_name}')".format(column_name=column_name)
                    if support_dict
                    else (
                        column_default != "CURRENT_TIMESTAMP" and column_default or None
                    )
                    and eval(column_default)
                )
            except:
                value = (
                    "kwargs.get('{column_name}')".format(column_name=column_name)
                    if support_dict
                    else (
                        column_default != "CURRENT_TIMESTAMP" and column_default or None
                    )
                    and column_default
                )

            if column_extra == "auto_increment" or column_default is not None:
                propertys += (
                    "# self.{column_name} = {value}  # type : {column_type} | allow_null : {is_nullable} | key : {column_key} | default_value : {column_default} | extra : {column_extra} | column_comment : {column_comment}".format(
                        column_name=column_name,
                        value=value,
                        column_type=column_type,
                        is_nullable=is_nullable,
                        column_key=column_key,
                        column_default=column_default,
                        column_extra=column_extra,
                        column_comment=column_comment,
                    )
                    + "\n"
                    + " " * 8
                )

            else:
                if value is None or isinstance(value, (float, int)) or support_dict:
                    propertys += (
                        "self.{column_name} = {value}  # type : {column_type} | allow_null : {is_nullable} | key : {column_key} | default_value : {column_default} | extra : {column_extra}| column_comment : {column_comment}".format(
                            column_name=column_name,
                            value=value,
                            column_type=column_type,
                            is_nullable=is_nullable,
                            column_key=column_key,
                            column_default=column_default,
                            column_extra=column_extra,
                            column_comment=column_comment,
                        )
                        + "\n"
                        + " " * 8
                    )
                else:
                    propertys += (
                        "self.{column_name} = '{value}'  # type : {column_type} | allow_null : {is_nullable} | key : {column_key} | default_value : {column_default} | extra : {column_extra}| column_comment : {column_comment}".format(
                            column_name=column_name,
                            value=value,
                            column_type=column_type,
                            is_nullable=is_nullable,
                            column_key=column_key,
                            column_default=column_default,
                            column_extra=column_extra,
                            column_comment=column_comment,
                        )
                        + "\n"
                        + " " * 8
                    )

        item_template = item_template.replace("${propertys}", propertys.strip())
        item_template = deal_file_info(item_template)

        return item_template

    def save_template_to_file(self, item_template, table_name):
        item_file = table_name + "_item.py"
        if os.path.exists(item_file):
            confirm = input("%s 文件已存在 是否覆盖 (y/n).  " % item_file)
            if confirm != "y":
                print("取消覆盖  退出")
                return

        with open(item_file, "w", encoding="utf-8") as file:
            file.write(item_template)
            print("\n%s 生成成功" % item_file)

        self._create_init.create()

    def create(self, tables_name, support_dict):
        input_tables_name = tables_name

        tables_name = self.select_tables_name(tables_name)
        if not tables_name:
            print(tables_name)
            tip = "mysql数据库中无 %s 表 " % input_tables_name
            raise KeyError(tip)

        for table_name in tables_name:
            table_name = table_name[0]
            table_name_hump_format = self.convert_table_name_to_hump(table_name)

            columns = self.select_columns(table_name)
            item_template = self.get_item_template()
            item_template = self.create_item(
                item_template, columns, table_name_hump_format, support_dict
            )
            self.save_template_to_file(item_template, table_name)


class CreateParser:
    def __init__(self):
        self._create_init = CreateInit()

    def cover_to_underline(self, key):
        regex = "[A-Z]*"
        capitals = re.findall(regex, key)

        if capitals:
            for pos, capital in enumerate(capitals):
                if not capital:
                    continue
                if pos == 0:
                    if len(capital) > 1:
                        key = key.replace(capital, capital.lower() + "_", 1)
                    else:
                        key = key.replace(capital, capital.lower(), 1)
                else:
                    if len(capital) > 1:
                        key = key.replace(capital, "_" + capital.lower() + "_", 1)
                    else:
                        key = key.replace(capital, "_" + capital.lower(), 1)

        return key

    def get_parser_template(self):
        templete_path = os.path.abspath(
            os.path.join(__file__, "../../templates/parser_template.tmpl")
        )
        with open(templete_path, "r", encoding="utf-8") as file:
            parser_template = file.read()

        return parser_template

    def create_parser(self, parser_template, parser_name):
        parser_template = parser_template.replace("${parser_name}", parser_name)
        parser_template = deal_file_info(parser_template)
        return parser_template

    def save_parser_to_file(self, parser, parser_name):
        parser_underline = self.cover_to_underline(parser_name)
        parser_file = parser_underline + ".py"

        if os.path.exists(parser_file):
            confirm = input("%s 文件已存在 是否覆盖 (y/n).  " % parser_file)
            if confirm != "y":
                print("取消覆盖  退出")
                return

        with open(parser_file, "w", encoding="utf-8") as file:
            file.write(parser)
            print("\n%s 生成成功" % parser_name)

        self._create_init.create()

    def create(self, parser_name):
        if parser_name.islower():
            parser_name = tools.key2hump(parser_name)
        parser_template = self.get_parser_template()
        parser = self.create_parser(parser_template, parser_name)
        self.save_parser_to_file(parser, parser_name)


class CreateProject:
    def copy_callback(self, src, dst, *, follow_symlinks=True):
        if src.endswith(".py"):
            with open(src, "r", encoding="utf-8") as src_file, open(
                dst, "w", encoding="utf8"
            ) as dst_file:
                content = src_file.read()
                content = deal_file_info(content)
                dst_file.write(content)

        else:
            shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

    def create(self, project_name):
        if os.path.exists(project_name):
            print("%s 项目已经存在" % project_name)
        else:
            templete_path = os.path.abspath(
                os.path.join(__file__, "../../templates/spider")
            )
            shutil.copytree(
                templete_path, project_name, copy_function=self.copy_callback
            )

            print("\n%s 项目生成成功" % project_name)


class CreateTable:
    def __init__(self):
        self._db = MysqlDB()

    def is_vaild_date(self, date):
        try:
            if ":" in date:
                time.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False

    def get_key_type(self, value):
        try:
            value = eval(value)
        except:
            value = value

        key_type = "varchar(255)"
        if isinstance(value, int):
            key_type = "int"
        elif isinstance(value, float):
            key_type = "double"
        elif isinstance(value, str):
            if self.is_vaild_date(value):
                if ":" in value:
                    key_type = "datetime"
                else:
                    key_type = "date"
            elif len(value) > 255:
                key_type = "text"
            else:
                key_type = "varchar(255)"

        return key_type

    def get_data(self):
        """
        @summary: 从控制台读取多行
        ---------
        ---------
        @result:
        """
        data = ""
        while True:
            line = sys.stdin.readline().strip()
            data += line
            if line == "}":
                break

        return tools.get_json(data)

    def create(self, table_name):
        # 输入表字段
        print('请输入表数据 json格式 如 {"name":"张三"}\n等待输入：\n')
        data = self.get_data()

        if not isinstance(data, dict):
            raise Exception("表数据格式不正确")

        # 拼接表结构
        sql = """
            CREATE TABLE `{db}`.`{table_name}` (
                `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id 自动递增',
                {other_key}
                `gtime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '抓取时间',
                PRIMARY KEY (`id`),
                {unique}
            ) COMMENT='';
        """

        print("请设置注释 回车跳过")
        other_key = ""
        for key, value in data.items():
            key = key2underline(key)
            key_type = self.get_key_type(value)

            comment = input("%s : %s  -> comment：" % (key, key_type))

            other_key += "`{key}` {key_type} COMMENT '{comment}',\n                ".format(
                key=key, key_type=key_type, comment=comment
            )

        print("\n")

        while True:
            is_need_batch_date = input("是否添加batch_date 字段 （y/n）:")
            if is_need_batch_date == "y":
                other_key += "`{key}` {key_type} COMMENT '{comment}',\n                ".format(
                    key="batch_date", key_type="date", comment="批次时间"
                )
                break
            elif is_need_batch_date == "n":
                break

        print("\n")

        while True:
            unique = input("请设置唯一索引, 多个逗号间隔\n等待输入：\n").replace("，", ",")
            if unique:
                break
        unique = "UNIQUE `idx` USING BTREE (`%s`) comment ''" % "`,`".join(
            unique.split(",")
        )

        sql = sql.format(
            db=setting.MYSQL_DB,
            table_name=table_name,
            other_key=other_key,
            unique=unique,
        )
        print(sql)
        self._db.execute(sql)
        print("\n%s 创建成功" % table_name)


class CreateInit:
    def create(self):
        __all__ = []

        import os

        path = os.getcwd()
        for file in os.listdir(path):
            if file.endswith(".py") and not file.startswith("__init__"):
                model = file.split(".")[0]
                __all__.append(model)

        del os

        with open("__init__.py", "w", encoding="utf-8") as file:
            text = "__all__ = %s" % dumps_json(__all__)
            file.write(text)


class CreateJson:
    def get_data(self):
        """
        @summary: 从控制台读取多行
        ---------
        ---------
        @result:
        """
        data = []
        while True:
            line = sys.stdin.readline().strip().replace("\t", " " * 4)
            if not line:
                break

            data.append(line)

        return data

    def create(self, sort_keys=False):
        contents = self.get_data()

        json = {}
        for content in contents:
            content = content.strip()
            if not content or content.startswith(":"):
                continue

            regex = "([^:\s]*)[:|\s]*(.*)"

            result = tools.get_info(content, regex, fetch_one=True)
            if result[0] in json:
                json[result[0]] = json[result[0]] + "&" + result[1]
            else:
                json[result[0]] = result[1].strip()

        print(tools.dumps_json(json, sort_keys=sort_keys))


def main():
    parser = argparse.ArgumentParser(description="模版生成器")

    parser.add_argument(
        "-i",
        "--item",
        nargs="+",
        help="创建item 如 create -i test 则生成test表对应的item。 支持like语法模糊匹配所要生产的表。 若想生成支持字典方式赋值的item，则create -item test 1",
        metavar="",
    )
    parser.add_argument(
        "-p", "--parser", help="创建parser 如 spider create -p TestParser", metavar=""
    )
    parser.add_argument(
        "-s", "--spider", help="创建爬虫项目 如 spider create -s test-spider", metavar=""
    )
    parser.add_argument(
        "-t", "--table", help="创建表 如 spider create -t table_name", metavar=""
    )
    parser.add_argument(
        "-init", help="创建__init__.py 如 spider create -init", action="store_true"
    )
    parser.add_argument("-j", "--json", help="创建json", action="store_true")
    parser.add_argument("-sj", "--sort_json", help="创建有序json", action="store_true")

    # 指定数据库
    parser.add_argument("--host", type=str, help="mysql 连接地址", metavar="")
    parser.add_argument("--port", type=str, help="mysql 端口", metavar="")
    parser.add_argument("--username", type=str, help="mysql 用户名", metavar="")
    parser.add_argument("--password", type=str, help="mysql 密码", metavar="")
    parser.add_argument("--db", type=str, help="mysql 数据库名", metavar="")

    args = parser.parse_args()

    if args.host:
        setting.MYSQL_IP = args.host
    if args.port:
        setting.MYSQL_PORT = int(args.port)
    if args.username:
        setting.MYSQL_USER_NAME = args.username
    if args.password:
        setting.MYSQL_USER_PASS = args.password
    if args.db:
        setting.MYSQL_DB = args.db

    if args.item:
        item_name, *support_dict = args.item
        support_dict = bool(support_dict)
        CreateItem().create(item_name, support_dict)

    elif args.parser:
        CreateParser().create(args.parser)

    elif args.spider:
        CreateProject().create(args.spider)

    elif args.table:
        CreateTable().create(args.table)

    elif args.init:
        CreateInit().create()

    elif args.json:
        CreateJson().create()

    elif args.sort_json:
        CreateJson().create(sort_keys=True)


if __name__ == "__main__":
    main()
