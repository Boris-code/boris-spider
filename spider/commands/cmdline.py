# -*- coding: utf-8 -*-
"""
Created on 2020/5/8 2:24 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
"""

import sys
from os.path import dirname, join

from spider.commands import create_builder
from spider.commands import shell


def _print_commands():
    with open(join(dirname(dirname(__file__)), "VERSION"), "rb") as f:
        version = f.read().decode("ascii").strip()

    print("Spider {}".format(version))
    print("\nUsage:")
    print("  spider <command> [options] [args]\n")
    print("Available commands:")
    cmds = {"create": "create spider、parser、item and so on", "shell": "debug response"}
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass))

    print('\nUse "spider <command> -h" to see more info about a command')


def execute():
    args = sys.argv
    if len(args) < 2:
        _print_commands()
        return

    command = args.pop(1)
    if command == "create":
        create_builder.main()
    elif command == "shell":
        shell.main()
    else:
        _print_commands()
