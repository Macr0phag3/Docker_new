# 安装基本组件
sudo yum -y install epel-release;
sudo yum install -y python-pip;
sudo yum install -y gcc;
sudo yum install -y wget;
sudo yum install -y git;
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python;
sudo pip install IPy;
sudo yum install -y python-devel
sudo pip install psutil
sudo pip install docker;
sudo pip install goto-statement;
sudo yum install -y yum-utils device-mapper-persistent-data lvm2;


# 开启 bridge-nf
sudo cat >> /etc/sysctl.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-arptables = 1
EOF

/sbin/sysctl -p

# 设置 iptables
systemctl stop firewalld

iptables -A DOCKER-m iprange --src-range 172.172.172.1-172.172.172.255 -j RETURN
iptables -A DOCKER-m iprange --dst-range 172.172.172.1-172.172.172.255 -j RETURN
iptables -A DOCKER-m iprange \! --src-range 172.172.172.1-172.172.172.255 -j DROP
ipset create allowthis hash:net
ipset add allowthis 192.168.12.1-192.168.12.7
ipset add allowthis 192.168.13.1
ipset add allowthis 192.168.0.2
iptables -A DOCKER-m set \! --match-set allowthis dst -j DROP

# 部署 Docker
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo;
sudo yum install -y docker-ce;
sudo systemctl start docker;
sudo systemctl enable docker;
docker version;

