# -*- coding: utf-8 -*-
import docker


def get_ip():
    for i in range(1, 128):
        yield "192.168.63.%d" % i


client = docker.APIClient(base_url='unix://var/run/docker.sock')
ips = get_ip()
images = [
    "registry.cn-qingdao.aliyuncs.com/hack_it/dns-zone",
    "registry.cn-qingdao.aliyuncs.com/hack_it/dns-reverse",
    "registry.cn-qingdao.aliyuncs.com/hack_it/hao_shop",
    "registry.cn-qingdao.aliyuncs.com/hack_it/yuzhong",
    "registry.cn-qingdao.aliyuncs.com/hack_it/svnvul",
    "registry.cn-qingdao.aliyuncs.com/hack_it/gitvul",
    "registry.cn-qingdao.aliyuncs.com/hack_it/lnmpmysql-webshell",
    "registry.cn-qingdao.aliyuncs.com/hack_it/lnmp-rsync",
    "registry.cn-qingdao.aliyuncs.com/hack_it/lnmp-openlist",
    "registry.cn-qingdao.aliyuncs.com/hack_it/rsync-nokey",
    "registry.cn-qingdao.aliyuncs.com/hack_it/mysql-weakey",
    "registry.cn-qingdao.aliyuncs.com/hack_it/ssh-weakey",
    "registry.cn-qingdao.aliyuncs.com/hack_it/s2-052",
    "registry.cn-qingdao.aliyuncs.com/hack_it/s2-048",
    "registry.cn-qingdao.aliyuncs.com/hack_it/s2-057",
    "registry.cn-qingdao.aliyuncs.com/hack_it/redis-nokey",
]

# for image in images:

image = "registry.cn-qingdao.aliyuncs.com/hack_it/dns-zone"
networking_config = client.create_networking_config(
    {
        'containers': client.create_endpoint_config(ipv4_address=ips.next(),)
    }
)

con = client.create_container(
    image, tty=True,
    detach=True, stdin_open=True,
    networking_config=networking_config,
    host_config=client.create_host_config(privileged=True),
)

client.start(container=con.get('Id'))
