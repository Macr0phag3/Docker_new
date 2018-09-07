# -*- coding:utf-8 -*-
import time


def log(msg, level, description, path):  # ok
    """
    记录事件，默认路径为 slave.py 所在路径
    log 文件名为 .slave_log

    参数:
    1. level: 事件等级
    2. description: 事件描述
    3. message: 事件原因的具体描述
    4. path: log 文件的路径(包括文件名)
    """

    with open(path, "a") as fp:
        fp.write("[%s]\nlevel: %s\ndescription: %s\nmessage: %s\n\n" %
                 (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), level, description.encode("utf8"), msg))


def put_color(string, color):  # ok
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "pink": "35",
        "cyan": "36",
        "white": "37",
    }
    return "\033[40;1;%s;40m%s\033[0m" % (colors[color], string)
