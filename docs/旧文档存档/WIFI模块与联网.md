# WIFI模块与联网

**先说明一些事情**

*我们将会创建一个 `wpa_supplicant`进程，用于管理无线网卡 `wlan0` 的连接，需要做一些必要的准备工作，首先创建一个控制接口目录，用于与管理工具（如 `wpa_cli`）进行通信，其次一个包含目标网络信息的配置文件。*

## 一、联网指令

*按照下面顺序即可实现连接WIFI*

**1、启用（激活）名为 `wlan0` 的无线网卡接口**

```bash
ifconfig wlan0 up
```

**2、创建一个用于存放 `wpa_supplicant` 进程通信文件的目录**

*`/var/run` 是 Linux 系统中一个特殊的临时运行时目录，主要用于存储系统运行过程中产生的临时文件、进程 PID 文件、套接字（socket）文件等与当前系统运行状态相关的数据。目录中的数据通常在系统重启后会被清空，所以可放心创建。*

```bash
mkdir -p /var/run/wpa_supplicant
```

**3、修改上述目录的权限，允许所有用户对该目录进行读写和执行操作**

```bash
chmod 777 /var/run/wpa_supplicant
```

**4、创建一个包含目标网络信息的配置文件(对于非开放网络)**

*`/tmp/` 是系统为所有用户（包括普通用户和程序）提供的临时文件存储空间。目录中的数据通常在系统重启后会被清空，所以可放心创建。*

```bash
cat > /tmp/wifi_config.conf << EOF
network={    
ssid="你的Wi-Fi名称"  
psk="你的Wi-Fi密码"  
key_mgmt=WPA-PSK
}
EOF
```

**创建一个包含目标网络信息的配置文件(对于开放网络）**

```bash
cat > /tmp/wifi_config.conf << EOF
network={    
ssid="你的Wi-Fi名称"
key_mgmt=NONE
}
EOF
```

**5、启动并加载新配置**

 *创建`wpa_supplicant` 进程，用于管理无线网卡 `wlan0` 的连接*

```bash
wpa_supplicant -i wlan0 -c /tmp/wifi_config.conf -C /var/run/wpa_supplicant/ -B
```

**6、查看状态（等待 `wpa_state=COMPLETED`）：**

```bash
wpa_cli -i wlan0 -p /var/run/wpa_supplicant/ status
```

## 二、其他指令

**1、禁用（关闭）名为 `wlan0` 的无线网卡接口**

```bash
ifconfig wlan0 down
```

**2、查找 `wpa_supplicant` 进程的 ID（PID）**

*我们只需要一个`wpa_supplicant`进程，如果不小心创建多个，可以用下面的指令查看存在 `wpa_supplicant`进程的ID，用于删除*

```bash
ps | grep wpa_supplicant | grep -v grep
```

**3、`kill` 命令终止进程**

```bash
kill -9 id
```

**4、通过 `wpa_cli`（`wpa_supplicant` 的命令行客户端）触发无线网络扫描**

```bash
wpa_cli -i wlan0 -p /var/run/wpa_supplicant/ scan
```

**5、获取并显示扫描结果**

```bash
wpa_cli -i wlan0 -p /var/run/wpa_supplicant/ scan_results
```

**6、获取IP**

```bash
ifconfig wlan0 | grep "inet"
```

**7、测试与百度连接**

```bash
ping -c 3 www.baidu.com
```

**8、ssh连接**

*如果你的开发板成功连接上了WIFI，并获取了IP，可以尝试使用下面的指令，实现开发板和电脑无线连接。*

```bash
ssh root@192.xxx.x.xxx
```

## 三、自动连接WIFI脚本

*验证这个脚本成功后可以把它设为启动任务，每次开机后自动连接WIFI*

```bash
#!/bin/bash

# Configuration parameters - Modify these according to your actual network
WIFI_INTERFACE="wlan0"           # Wireless network interface name
SSID="你的WIFI名称"               # Wireless network name
KEY_MGMT="WPA-PSK"               # Authentication method: NONE(open), WPA-PSK(encrypted)
PSK="你的Wi-Fi密码"               # Wireless network password (fill for encrypted networks)

# Function: Print info and execute command
run_command() {
    echo "Executing: $1"
    eval $1
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "Command failed with exit code: $exit_code"
        exit $exit_code
    fi
}

echo "===== Starting automatic network connection ====="

# 1. Activate wireless interface
echo "1. Activating wireless interface $WIFI_INTERFACE..."
run_command "ifconfig $WIFI_INTERFACE up"

# 2. Prepare wpa_supplicant environment
echo -e "\n2. Preparing wpa_supplicant runtime environment..."
run_command "mkdir -p /var/run/wpa_supplicant"
run_command "chmod 777 /var/run/wpa_supplicant"

# 3. Create WiFi configuration file
echo -e "\n3. Creating WiFi configuration file..."
CONFIG_FILE="/tmp/wifi_config.conf"
run_command "rm -f $CONFIG_FILE"  # Remove old configuration file

# Write configuration content
echo "network={" >> $CONFIG_FILE
echo "    ssid=\"$SSID\"" >> $CONFIG_FILE
echo "    key_mgmt=$KEY_MGMT" >> $CONFIG_FILE

# Add password for encrypted networks
if [ "$KEY_MGMT" = "WPA-PSK" ] && [ -n "$PSK" ]; then
    echo "    psk=\"$PSK\"" >> $CONFIG_FILE
fi

echo "}" >> $CONFIG_FILE

echo "Configuration file content:"
cat $CONFIG_FILE

# 4. Start wpa_supplicant to connect network
echo -e "\n4. Connecting to $SSID ..."
run_command "wpa_supplicant -i $WIFI_INTERFACE -c $CONFIG_FILE -C /var/run/wpa_supplicant/ -B"

# Wait for connection establishment
echo -e "\n5. Waiting for network connection (5 seconds)..."
sleep 5

# 6. Obtain IP address via DHCP
echo -e "\n6. Obtaining IP address..."
# Try udhcpc (common in embedded systems)
if command -v udhcpc &> /dev/null; then
    run_command "udhcpc -i $WIFI_INTERFACE"
else
    # Try dhclient (common in desktop systems)
    run_command "dhclient $WIFI_INTERFACE"
fi

# 7. Display connection result
echo -e "\n===== Network connection completed! Current status ====="
ifconfig $WIFI_INTERFACE

exit 0
```
