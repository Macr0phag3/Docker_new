# -*- coding: utf-8 -*-
from toolboxs import stoolbox as st
from toolboxs import ptoolbox as pt
from goto import with_goto
from pprint import pprint
import sys
import signal
import json


def abort(a, b):
    sys.exit("\nBye~")


def cls():
    print "\033c"


@with_goto
def Main_menu():
    label .main
    choice = raw_input(
        """
=============
输入数字以继续:
1. 桥接
2. 取消桥接
3: 显示负载
4: 显示已用 ip
0. 退出
=============
输入数字以继续: """
    )
    cls()
    setting = st.setting
    subnet = setting["bridge"]["subnet"]
    self_ip = setting["bridge"]["self_ip"]
    iface = setting["bridge"]["iface"]
    gateway = setting["bridge"]["gateway"]

    if choice == '1':
        result = json.loads(st.nk_bridge(subnet, self_ip, iface, gateway))
        if result["code"]:
            print pt.put_color("桥接失败", "red")
            print result["msg"]
        else:
            print pt.put_color("桥接成功", "green")

    elif choice == '2':
        result = json.loads(st.nk_unbridge())
        if result["code"]:
            print pt.put_color("取消桥接失败", "red")
            print result["msg"]
        else:
            print pt.put_color("取消桥接成功", "green")

    elif choice == '3':
        pprint(st.loads_ls())

    elif choice == '4':
        pprint(st.ip_used_ls(subnet))

    elif choice == '0':
        sys.exit("Bye~")

    else:
        print pt.put_color("输入有误, 重新输入", "red")

    goto .main


signal.signal(signal.SIGINT, abort)
signal.signal(signal.SIGTERM, abort)
Main_menu()
