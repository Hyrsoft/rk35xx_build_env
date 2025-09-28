不给buildroot引入lsblk工具的前提下查看并挂载sd卡

sd卡插拔前后

```bash
root@rk3506-buildroot:~# cat /proc/partitions
major minor  #blocks  name

  31        0       4096 mtdblock0
  31        1       1024 mtdblock1
  31        2        256 mtdblock2
  31        3      25600 mtdblock3
  31        4      15360 mtdblock4
  31        5     143360 mtdblock5
  31        6      16384 mtdblock6
  31        7      51328 mtdblock7
root@rk3506-buildroot:~# cat /proc/partitions
major minor  #blocks  name

  31        0       4096 mtdblock0
  31        1       1024 mtdblock1
  31        2        256 mtdblock2
  31        3      25600 mtdblock3
  31        4      15360 mtdblock4
  31        5     143360 mtdblock5
  31        6      16384 mtdblock6
  31        7      51328 mtdblock7
 179        0    8049664 mmcblk0
```

进行格式化 在电脑上进行操作

```bash
~ 
❯ sudo mkfs.ext4 /dev/sda
[sudo] hao 的密码：
mke2fs 1.47.2 (1-Jan-2025)
创建含有 2012416 个块（每块 4k）和 503936 个 inode 的文件系统
文件系统 UUID：e62a3654-8e50-4dbe-807d-5df876a07226
超级块的备份存储于下列块：
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

正在分配组表：完成                            
正在写入 inode表：完成                            
创建日志（16384 个块）：完成
写入超级块和文件系统账户统计信息：已完成
```

我这张sd卡格式化成ext4，开发板无法挂载，使用vfat格式，可以正常挂载

```bash
❯ sudo mkfs.vfat -F 32 /dev/sda
mkfs.fat 4.2 (2021-01-31)
```

```bash
root@rk3506-buildroot:~# mount -t vfat /dev/mmcblk0 /sdcard
root@rk3506-buildroot:~# df -h
Filesystem                Size      Used Available Use% Mounted on
ubi0:rootfs             112.8M     64.9M     47.9M  58% /
devtmpfs                112.1M         0    112.1M   0% /dev
tmpfs                   112.2M    280.0K    111.9M   0% /var/log
tmpfs                   112.2M      8.0K    112.2M   0% /tmp
tmpfs                   112.2M    228.0K    112.0M   0% /run
tmpfs                   112.2M         0    112.2M   0% /dev/shm
/dev/ubi7_0              38.0M    384.0K     37.6M   1% /userdata
/dev/ubi6_0               5.6M      4.2M      1.4M  75% /oem
/dev/mmcblk0              7.7G      4.0K      7.7G   0% /mnt/sdcard
/dev/mmcblk0              7.7G      4.0K      7.7G   0% /mnt/sdcard
```

但是它并不会挂载到我预设的/sdcard上，而是挂载到了/mnt/sdcard上

查看规则

```bash
root@rk3506-buildroot:~# cat /etc/fstab
# <file system> 		<mount pt>      	<type>  		<options>       				<dump>  <pass>
/dev/root       		/               	auto    		rw,noauto       				0       1
tmpfs           		/tmp            	tmpfs   		mode=1777       				0       0
tmpfs           		/run            	tmpfs   		mode=0755,nosuid,nodev  		0       0
tmpfs           		/var/log        	tmpfs   		mode=0755,nosuid,nodev  		0       0
proc    				/proc   			proc    		defaults        				0 		0
devtmpfs        		/dev    			devtmpfs        defaults        				0 		0
devpts  				/dev/pts        	devpts  		mode=0620,ptmxmode=0000,gid=5   0 		0
tmpfs   				/dev/shm        	tmpfs   		nosuid,nodev,noexec     		0 		0
sysfs   				/sys    			sysfs   		nosuid,nodev,noexec     		0 		0
configfs        		/sys/kernel/config  configfs        defaults        				0 		0
debugfs 				/sys/kernel/debug   debugfs 		defaults        				0 		0
pstore  				/sys/fs/pstore  	pstore  		nosuid,nodev,noexec     		0 		0
PARTLABEL=oem   		/oem    			ubi     		defaults        				0 		2
PARTLABEL=userdata      /userdata       	ubi     		defaults        				0 		2
```

