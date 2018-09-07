# -*- coding: utf-8 -*-
from toolboxs import mtoolbox as mt
from toolboxs import ptoolbox as pt
from goto import with_goto
from pprint import pprint
import sys
import signal
import json
import random


def exit(a=None, b=None):  # ok
    show_logo()
    sys.exit(pt.put_color(
        random.choice([
            "Goodbye", "Have a nice day",
            "See you later", "Bye",
            "Farewell", "Cheerio",
        ]), "white"))


def colored_choice(num):
    num_color = [pt.put_color(str(i), "cyan") for i in range(num)]
    alpha_color = [pt.put_color(i, "yellow") for i in ['b', 'q']]
    return num_color + alpha_color


def cls():  # ok
    print "\033c"


def show_logo():  # ok
    cls()
    print """
    %s\
    %s\
%s""" % (pt.put_color("""
      .-""`""-.
  __/`oOoOoOoOo`\__
  '.-=-=-=-=-=-=-.'
    `-=.=-.-=.=-'
       ^  ^  ^\
    """, "yellow"),  pt.put_color("""
hack it and docker it
""", "green"), pt.put_color("======================\n", "white"))


@with_goto
def Main_menu():  # ok
    label .main
    choice = raw_input("""
==========
{}: 基本操作
{}: 更多操作
{}: 使用说明
{}: 退出
==========
> """.format(*[i for i in colored_choice(3) if "b" not in i]))

    show_logo()
    if choice == '0':
        basic_menu()

    elif choice == '1':
        pro_menu()

    elif choice == '2':
        intro_menu()

    elif choice == 'q':
        exit()

    else:
        print pt.put_color("输入有误, 重新输入", "red")

    goto .main


@with_goto
def basic_menu():
    label .basic_menu
    choice = raw_input("""
==================
{}: 分配容器
{}: 回收容器
{}: 查看镜像
{}: 查看容器
{}: 检查连接
{}: 详细信息
{}: 返回
{}: 退出
==================
> """.format(*colored_choice(6)))

    show_logo()
    if choice == "0":
        result = json.loads(mt.ip_assign(subnet))
        if result["code"]:
            print pt.put_color(u"[X]分配 ip 失败", "red")
            print "  [-]", result["msg"]
            goto .basic_menu

        container_ip = result["result"]
        result = json.loads(mt.check_load())
        if result["code"]:
            print pt.put_color(u"[X]负载查询失败", "red")
            print "  [-]", result["msg"]
            goto .basic_menu

        min_load = 100
        for i in result["result"]:
            for j in i:
                value = i[j]["cpu"]*0.2 + i[j]["mem"]*0.8
                if value < min_load:
                    min_load = value
                    ip = j

        image_list = json.loads(mt.command2slave(ip, json.dumps({
            "mission": "cmd2docker",
            "commands": {
                "command": "images_ls",
                "arg": []
            }})))

        if image_list["code"]:
            print pt.put_color(u"[X]获取虚拟机: %s 的所有镜像失败" % ip, "red")
            print "  [-]", image_list["msg"]
            goto .basic_menu

        print u"选择镜像"
        label .image_list
        print "=" * 50
        for i, image in enumerate(image_list["result"]):
            print "%s: %s" % (pt.put_color(str(i), "cyan"), image)
        print "=" * 50

        choice_image = raw_input("> ")
        if choice_image == "":
            show_logo()
            print pt.put_color(u"[!]操作已取消", "yellow")
            goto .basic_menu

        elif choice_image not in [str(c) for c in range(i+1)]:
            show_logo()
            print pt.put_color(u"[X]输入有误, 重新输入", "red")
            goto .image_list

        image_name = image_list["result"][int(choice_image)]
        result = json.loads(
            mt.command2slave(
                ip, json.dumps({
                    "mission": "cmd2docker",
                    "commands": {
                        "command": "run",
                        "arg": [image_name, container_ip]
                    }})))

        if result["code"]:
            print pt.put_color(u"[X]启动容器失败", "red")
            print u"  [-]", result["msg"]
            goto .basic_menu

        print pt.put_color(u"[+]启动镜像 %s 的容器成功" % image_name, "green")
        print u"  [-]容器位于虚拟机 %s 中" % pt.put_color(ip, "white")
        print u"  [-]给容器分配的 ip 为:", pt.put_color(result["result"]["ip"], "white")
        print u"  [-]ID 为", pt.put_color(result["result"]["id"], "white")

    elif choice == '1':
        mission = {
            "mission": "cmd2docker",
            "commands": {
                "command": "others_cmd",
                "arg": []
            }}

        label .slave_list
        print u"选择虚拟机"
        print "-"*50
        alive_slave = []
        empty_slave = []

        results = []
        for i, ip in enumerate(ips):
            result = json.loads(
                mt.command2slave(
                    ip, json.dumps({
                        "mission": "cmd2docker",
                        "commands": {
                            "command": "containers_ls",
                            "arg": []
                        }})))

            results.append(result)

            if result["code"]:
                print u"%s: 虚拟机: %s" % (i, pt.put_color(ip, "red"))
                print "  [X]error:", result["msg"]

            alive_slave.append(i)
            print "%s: %s" % (pt.put_color(str(i), "cyan"), pt.put_color(ip, "green"))
            if result["result"] == []:
                print pt.put_color("  [!]Empty", "yellow")
                empty_slave.append(i)
            else:
                for j, r in enumerate(result["result"]):
                    print "  %s: [%s] [%s] [%s]" % (pt.put_color(str(j), "cyan"), pt.put_color(r["status"], "white"),
                                                    pt.put_color(r["ip"], "white"), pt.put_color(r["image name"], "white"))

        print "\n{}: 返回\n{}: 退出".format(*colored_choice(0))
        print "-"*50

        choice_slave = raw_input("> ")
        if choice_slave == 'b':
            show_logo()
            goto .basic_menu

        elif choice_slave == 'q':
            exit()

        elif not choice_slave.isdigit():
            show_logo()
            print pt.put_color(u"输入有误, 重新输入", "red")
            goto .slave_list

        choice_slave = int(choice_slave)
        if choice_slave not in alive_slave:
            show_logo()
            print pt.put_color(u"此虚拟机无法连接, 重新选择", "red")
            goto .slave_list

        elif choice_slave in empty_slave:
            show_logo()
            print pt.put_color(u"此虚拟机无容器, 重新选择", "red")
            goto .slave_list

        ip = ips[choice_slave]
        choice_container = raw_input(
            "\n选择容器\n=========\n{}: 返回\n{}: 退出\n=========\n> ".format(*colored_choice(0)))

        if choice_container == 'b':
            show_logo()
            goto .slave_list

        elif choice_container == 'q':
            exit()

        elif not choice_container.isdigit():
            show_logo()
            print pt.put_color(u"输入有误, 重新输入", "red")
            goto .slave_list

        choice_container = int(choice_container)
        if choice_container not in range(len(results[choice_slave]["result"])):
            show_logo()
            print pt.put_color(u"虚拟机: %s 无此容器, 重新选择" % ip, "red")
            goto .slave_list

        id_or_name = results[choice_slave]["result"][choice_container]["id"]
        show_logo()
        print u"[+]回收容器:", id_or_name
        mission["commands"]["arg"] = [id_or_name, "kill"]
        print u"  [-]停止容器 ...",
        result = json.loads(mt.command2slave(ip, json.dumps(mission)))

        if result["code"]:
            print pt.put_color(u"失败", "red")
            print u"  [x]" + result["msg"]
            goto .basic_menu

        print pt.put_color(u"成功", "green")
        print u"  [-]删除容器 ...",
        mission["commands"]["arg"] = [id_or_name, "rm"]
        result = json.loads(mt.command2slave(
            ip, json.dumps(mission)))

        if result["code"]:
            print pt.put_color(u"失败", "red")
            print u"  [x]" + result["msg"]
            goto .basic_menu

        print pt.put_color(u"成功", "green")
        print u"[!]完成"

    elif choice == "2":
        show_logo()
        image_list = json.loads(mt.command2slave("192.168.12.1", json.dumps({
            "mission": "cmd2docker",
            "commands": {
                "command": "images_ls",
                "arg": []
            }})))

        if image_list["code"]:
            print pt.put_color(u"[X]获取虚拟机: 192.168.12.1 的所有镜像失败", "red")
            print u"  [-]", image_list["msg"]
            return

        images = image_list["result"]
        for i, image in enumerate(images):
            print "%s: %s" % (pt.put_color(str(i), "cyan"), image)

    elif choice == "3":
        mission = {
            "mission": "cmd2docker",
            "commands": {
                "command": "containers_ls",
                "arg": []
            }
        }

        results = []
        for i, ip in enumerate(ips):
            result = json.loads(mt.command2slave(ip, json.dumps(mission)))
            if result["code"]:
                print u"[X]获取虚拟机 %s 的所有容器失败" % ip
                continue

            results.extend(result["result"])

        for i, container in enumerate(results):
            print "%s. %s" % (pt.put_color(str(i), "cyan"),
                              pt.put_color(container["id"][:6], "white"))
            print "  [-]id: "+container["id"]
            print u"  [-]状态: "+pt.put_color(container["status"],
                                            "green" if container["status"] == "running" else "yellow")
            print u"  [-]启动时间点: "+pt.put_color(container["start time"], "blue")
            print u"  [-]容器 ip: "+pt.put_color(container["ip"], "white")
            print u"  [-]所在虚拟机 ip: "+pt.put_color(container["slave ip"], "white")
            print u"  [-]镜像名: "+pt.put_color(container["image name"], "white")
            print "-"*50, '\n'

    elif choice == '4':
        mission = {
            "mission": "cmd2slave",
            "commands": {
                "command": "check_alive",
                "arg": [subnet]
            }
        }

        for ip in ips:
            result = json.loads(mt.command2slave(ip, json.dumps(mission), timeout=10))
            if result["code"]:
                print pt.put_color(ip, "red"), pt.put_color(
                    u"内网", "red"), pt.put_color(u"外网", "red")
            else:
                if result["result"]:
                    print pt.put_color(ip, "yellow"), pt.put_color(
                        u"内网", "green"), pt.put_color(u"外网", "red")
                else:
                    print pt.put_color(ip, "green"), pt.put_color(
                        u"内网", "green"), pt.put_color(u"外网", "green")

    elif choice == "5":
        slaves_info = {}
        mission = [
            {
                "mission": "cmd2docker",
                "commands":
                {
                    "command": "images_ls",
                    "arg": [],
                }
            },
            {
                "mission": "cmd2docker",
                "commands":
                {
                    "command": "containers_ls",
                    "arg": [],
                }
            }
        ]

        for ip in ips:
            slaves_info[ip] = {
                "image": {
                    "code": 1,
                    "msg": "",
                    "images": []
                },
                "container": {
                    "code": 1,
                    "msg": "",
                    "containers": []
                }
            }

            result = json.loads(mt.command2slave(ip, json.dumps(mission)))
            print u"[+]虚拟机: "+pt.put_color(ip, "white")

            if result[0]["code"]:
                print pt.put_color(u"  [X]镜像", "red")
                print "    [-]error: "+result[0]["msg"]
            else:
                print u"  [-]镜像(%s)" % pt.put_color(str(len(result[0]["result"])), "cyan")
                for image in result[0]["result"]:
                    print "    [-]"+image

            if result[1]["code"]:
                print pt.put_color(u"\n  [X]容器", "red")
                print "    [-]error: "+result[1]["msg"]
            else:
                print u"\n  [-]容器(%s)" % pt.put_color(
                    str(len(result[1]["result"])), "cyan")
                for container in result[1]["result"]:
                    print "    [-]short id: "+pt.put_color(container["id"][:6], "white")
                    print u"      [-]启动时间点: "+pt.put_color(container["start time"], "blue")
                    print u"      [-]状态: "+pt.put_color(container["status"],
                                                        "green" if container["status"] == "running" else "yellow")
                    print u"      [-]容器 ip: "+pt.put_color(container["ip"], "white")
                    print "      [-]id: "+container["id"]
                    print u"      [-]镜像名: "+pt.put_color(container["image name"], "white"), "\n"
            print "-"*50, '\n'

    elif choice == 'b':
        return

    elif choice == 'q':
        exit()

    else:
        print pt.put_color(u"输入有误, 重新输入", "red")

    goto .basic_menu


def pro_menu():
    print u"\033[40;1;33;40m施工中...\033[0m"


def intro_menu():
    print """\033[40;1;36;40m1\033[0m. 输入行首的数字以选择对应的选项。
\033[40;1;36;40m2\033[0m. 输入 \033[40;1;33;40mb\033[0m 总是返回上一级。
\033[40;1;36;40m3\033[0m. 输入 \033[40;1;33;40mq\033[0m 总是直接退出程序。
\033[40;1;36;40m4\033[0m. 在更多操作中，在输入信息（如 ip 等）时，输入为 \033[40;1;37;40m空\033[0m（即直接回车），则为放弃当前操作。
\033[40;1;36;40m5\033[0m. \033[40;1;37;40m基本操作\033[0m 菜单中，涵盖绝大多数使用场景，无特殊情况只需要使用这些功能即可。
\033[40;1;36;40m6\033[0m. \033[40;1;37;40m更多操作\033[0m 菜单中，有很多底层的细节操作，有特殊需求可以使用这些功能。"""


signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

ips = mt.setting["slave_ip"]
subnet = mt.setting["bridge"]["subnet"]

show_logo()
Main_menu()
