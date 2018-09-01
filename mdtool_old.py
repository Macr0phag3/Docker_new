
@with_goto
def notrun(command):  # ok
    label .notrun
    choice = raw_input("""
===========
{}: 单个容器
{}: 多个容器
{}: 所有容器
{}: 返回
{}: 退出
========+==
> """.format(*colored_choice(3)))

    if choice not in ['b', '1', '2', '3', 'q']:
        show_logo()
        print pt.put_color("输入有误, 重新输入", "red")
        goto .notrun

    if choice == 'b':
        return show_logo()

    elif choice == 'q':
        abort(1, 1)

    ip = raw_input("输入容器所在的虚拟机的 ip：")
    if ip == "":
        show_logo()
        print pt.put_color(u"操作已取消", "yellow")
        goto .notrun

    mission = {
        "mission": "cmd2docker",
        "commands": {
            "command": "others_cmd",
            "arg": []
        }
    }

    show_logo()
    if choice == "1":
        names = [raw_input("输入容器的 id 或名字: ")]
        if names == [""]:
            show_logo()
            print pt.put_color(u"操作已取消", "yellow")
            goto .notrun

    elif choice == "2":
        names = raw_input("输入容器的 id 或名字 (用单个空格隔开): ").split(" ")
        if names == [""]:
            show_logo()
            print pt.put_color(u"操作已取消", "yellow")
            goto .notrun

    elif choice == "3":
        mission["commands"]["command"] = "containers_ls"
        result = json.loads(mt.command2slave(ip, json.dumps(mission)))
        if result["code"]:
            print pt.put_color("获得 %s 的所有容器失败" % ip, "red")
            print result["msg"]
        else:
            names = []
            name = result["result"]
            for i in name:
                names.append(i["id"])
        mission["commands"]["command"] = "others_cmd"

    for name in names:
        mission["commands"]["arg"] = [name, command]
        pprint(mt.command2slave(ip, json.dumps(mission)))


@with_goto
def dk_menu():  # ok
    label .docker
    choice = raw_input("""
===========
{}: 分配容器
{}: 回收容器
{}: 查看信息
{}: 列出镜像
{}: 更多操作
{}: 返回
{}: 退出
===========
> """.format(*colored_choice(5)))

    show_logo()

    elif choice == "3":
        slaves_info = {}
        ips = get_setting("slave_ip")

        results = command2all_slaves(ips, "images_ls")
        for i, result in enumerate(results):
            slaves_info[ips[i]] = {
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

            if result["code"]:
                slaves_info[ips[i]]["image"]["msg"] = result["msg"]
            else:
                slaves_info[ips[i]]["image"]["code"] = 0
                slaves_info[ips[i]]["image"]["images"] = result["result"]

        results = command2all_slaves(ips, "containers_ls")
        for i, result in enumerate(results):
            if result["code"]:
                slaves_info[ips[i]]["container"]["msg"] = result["msg"]
            else:
                slaves_info[ips[i]]["container"]["code"] = 0
                slaves_info[ips[i]]["container"]["containers"] = result["result"]

        for ip in ips:
            print "[+]slave: "+pt.put_color(ip, "white")

            images_info = slaves_info[ip]["image"]
            if images_info["code"]:
                print pt.put_color("  [X]images", "red")
                print "    [-]error: "+images_info["msg"]
            else:
                print "  [-]images(%s)" % pt.put_color(str(len(images_info["images"])), "blue")
                for image in images_info["images"]:
                    print "    [-]"+image

            containers_info = slaves_info[ip]["container"]
            if containers_info["code"]:
                print pt.put_color("\n  [X]containers", "red")
                print "    [-]error: "+containers_info["msg"]
            else:
                print "\n  [-]containers(%s)" % pt.put_color(
                    str(len(containers_info["containers"])), "blue")
                for container in containers_info["containers"]:
                    print "    [-]short id: "+pt.put_color(container["id"][:6], "white")
                    print "      [-]ip: "+pt.put_color(container["ip"], "white")
                    print "      [-]id: "+container["id"]
                    print "      [-]status: "+pt.put_color(container["status"],
                                                           "green" if container["status"] == "running" else "yellow")
                    print "      [-]image name: "+pt.put_color(container["image name"], "white")
                    print

            print "-"*50

    elif choice == "4":
        show_logo()
        image_list = json.loads(mt.command2slave("192.168.12.1", json.dumps({
            "mission": "cmd2docker",
            "commands": {
                "command": "images_ls",
                "arg": []
            }})))

        if image_list["code"]:
            print pt.put_color(u"获取虚拟机: 192.168.12.1 的所有镜像失败", "red")
            print u"原因如下:\n", image_list["msg"]
            return

        images = image_list["result"]
        for i, image in enumerate(images):
            print "%s: %s" % (pt.put_color(str(i), "blue"), image)

    elif choice == "5":
        dk_more_menu()

    elif choice == 'b':
        return

    elif choice == 'q':
        abort(1, 1)

    else:
        print pt.put_color(u"输入有误, 重新输入", "red")

    goto .docker


def command2all_slaves(ips, command):
    result = []
    for ip in ips:
        mission = {
            "mission": "cmd2docker",
            "commands": {
                "command": command,
                "arg": []
            }
        }
        result.append(json.loads(mt.command2slave(ip, json.dumps(mission))))
    return result


@with_goto
def dk_more_menu():
    label .dk_more_menu
    choice = raw_input("""
=======
{}: 运行
{}: 暂停
{}: 恢复
{}: 停止
{}: 删除
{}: 列出
{}: 负载
{}: 返回
{}: 退出
=======
> """.format(*colored_choice(7)))

    show_logo()

    if choice == "1":
        ip = raw_input(u"输入分配容器的虚拟机的 ip: ")
        if ip == "":
            show_logo()
            print pt.put_color(u"操作已取消", "yellow")
            goto .dk_more_menu

        image_name = raw_input(u"输入镜像名（必要时加上版本号）: ")
        if image_name == "":
            show_logo()
            print pt.put_color(u"操作已取消", "yellow")
            goto .dk_more_menu

        container_ip = raw_input(u"输入给容器分配的 ip: ")
        if container_ip == "":
            show_logo()
            print pt.put_color(u"操作已取消", "yellow")
            goto .dk_more_menu

        subnet = get_setting("bridge")["subnet"]
        result = json.loads(mt.ip_assign(subnet, container_ip))
        if result["code"]:
            print pt.put_color(u"指定 ip 失败", "red")
            print u"原因如下:\n", result["msg"]
        else:
            container_ip = result["result"]
            result = json.loads(
                mt.command2slave(
                    ip, json.dumps({
                        "mission": "cmd2docker",
                        "commands": {
                            "command": "run",
                            "arg": [image_name, container_ip]
                        }})))

            if result["code"]:
                print pt.put_color("启动容器失败", "red")
                print "原因如下:\n", result["msg"]
            else:
                print pt.put_color(u"[+]启动容器 %s 成功" % image_name, "green")
                print u"  [-]位于虚拟机 %s 中" % pt.put_color(ip, "white")
                print u"  [-]容器分配的 ip 为:", pt.put_color(result["result"]["ip"], "white")
                print u"  [-]ID 为", pt.put_color(result["result"]["id"], "white")

    elif choice in ["2", "3", "4", "5"]:
        command = {
            "2": "pause",
            "3": "unpause",
            "4": "kill",
            "5": "rm",
        }
        notrun(command[choice])

    elif choice == "6":
        label .container_or_image
        choice = raw_input("""
=======
{}: 容器
{}: 镜像
{}: 返回
{}: 退出
=======
> """.format(*colored_choice(2)))

        choice_list = {
            "1": "containers_ls",
            "2": "images_ls",
        }

        show_logo()

        if choice not in ['b', '1', '2', 'q']:
            print pt.put_color("输入有误, 重新输入", "red")
            goto .container_or_image

        if choice == 'b':
            goto .dk_more_menu

        elif choice == 'q':
            abort(1, 1)

        choice = choice_list[choice]
        label .ms
        ip_num = raw_input("""
=============
{}: 单台虚拟机
{}: 多台虚拟机
{}: 所有虚拟机
{}: 返回
{}: 退出
=============
> """.format(*colored_choice(3)))

        show_logo()
        if ip_num not in ['b', '1', '2', '3', 'q']:
            print pt.put_color("输入有误, 重新输入", "red")
            goto .ms

        if ip_num == "1":
            ips = [raw_input("输入虚拟机的 ip: ")]
            if ips == [""]:
                show_logo()
                print pt.put_color(u"操作已取消", "yellow")
                goto .ms

        elif ip_num == "2":
            ips = raw_input("输入 ip(用单个空格隔开): ").split(" ")
            if ips == [""]:
                show_logo()
                print pt.put_color(u"操作已取消", "yellow")
                goto .ms

        elif ip_num == "3":
            ips = get_setting("slave_ip")

        elif ip_num == 'b':
            goto .container_or_image

        elif ip_num == 'q':
            abort(1, 1)

        results = command2all_slaves(ips, choice)
        for i, result in enumerate(results):
            if result["code"]:
                print "[+]slave:", pt.put_color(ips[i], "red")
                print "  [-]error:", result["msg"]
            else:
                print "[+]slave:", pt.put_color(ips[i], "green")
                print "  [-]result:"
                pprint(result["result"])
                print

    elif choice == "7":
        result = json.loads(mt.check_load())

        if result["code"]:
            print pt.put_color("负载查询失败", "red")
            print "原因如下:\n", result["msg"]
        else:
            print pt.put_color("负载查询成功", "green")
            print u"结果如下"
            pprint(result["result"])

    elif choice == 'b':
        return

    elif choice == 'q':
        abort(1, 1)

    else:
        print pt.put_color("输入有误, 重新输入", "red")

    goto .dk_more_menu
