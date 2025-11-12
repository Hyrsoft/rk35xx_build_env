#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil

# --- 用户配置 ---
# 在这里修改为您要挂载的根文件系统的绝对路径
ROOTFS_PATH = "/home/hao/projects/EVB3506_SDK/alpine_rootfs"

# 请指定 QEMU 静态二进制文件的路径。
# 通常在 /usr/bin/ 目录下, 例如 qemu-aarch64-static, qemu-arm-static 等。
QEMU_STATIC_BINARY = "/usr/bin/qemu-arm-static"
# --- 配置结束 ---


def run_command(command, check=True):
    """执行一个 shell 命令并处理可能发生的错误"""
    print(f"🚀 执行: {' '.join(command)}")
    try:
        subprocess.run(command, check=check)
    except FileNotFoundError:
        print(f"❌ 命令未找到: {command[0]}。请确保该程序已安装并在 PATH 环境变量中。", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {' '.join(e.cmd)} (返回码: {e.returncode})", file=sys.stderr)
        if e.stdout: print(f"   stdout: {e.stdout.decode()}", file=sys.stderr)
        if e.stderr: print(f"   stderr: {e.stderr.decode()}", file=sys.stderr)
        if not check: # 如果允许失败，只打印警告
             print("   (警告: 此命令失败，但程序将继续执行)")
        else: # 如果要求成功，则退出
            sys.exit(1)


def unmount_filesystems():
    """
    按正确顺序卸载所有 chroot 文件系统。
    会检查每个挂载点是否存在且已挂载。
    """
    print("\n🧹 开始安全卸载程序...")

    # 挂载点列表，按卸载的正确顺序（与挂载顺序相反）排列
    mount_points = [
        'dev/pts',
        'dev',
        'sys',
        'proc'
    ]

    for mp in mount_points:
        target_path = os.path.join(ROOTFS_PATH, mp)
        # 检查路径是否存在并且确实是一个挂载点
        if os.path.exists(target_path) and os.path.ismount(target_path):
            run_command(['sudo', 'umount', target_path], check=False) # 允许失败，以防万一

    # 清理 QEMU 模拟器
    if QEMU_STATIC_BINARY:
        qemu_dest_path = os.path.join(ROOTFS_PATH, 'usr', 'bin', os.path.basename(QEMU_STATIC_BINARY))
        if os.path.exists(qemu_dest_path):
            print(f"   清理 QEMU 模拟器: {qemu_dest_path}")
            run_command(['sudo', 'rm', qemu_dest_path])

    print("✅ 清理完成。")


def mount_and_chroot():
    """
    挂载所需的文件系统并进入 chroot 环境。
    使用 try...finally 确保无论 chroot 内部发生什么，都会执行卸载。
    """
    try:
        print("🛠️  开始挂载 chroot 所需的文件系统...")

        # 定义要挂载的内容 (源, 目标子目录, 类型, 选项)
        mounts = [
            ('proc', 'proc', 'proc', None),
            ('sysfs', 'sys', 'sysfs', None),
            ('/dev', 'dev', None, 'bind'),
            ('/dev/pts', 'dev/pts', None, 'bind'),
        ]

        for source, dest_subdir, fstype, options in mounts:
            target_path = os.path.join(ROOTFS_PATH, dest_subdir)
            if not os.path.exists(target_path):
                print(f"   创建缺失的目录: {target_path}")
                run_command(['sudo', 'mkdir', '-p', target_path])

            command = ['sudo', 'mount']
            if fstype:
                command.extend(['-t', fstype])
            if options == 'bind':
                command.extend(['-o', 'bind'])
            
            command.extend([source, target_path])
            run_command(command)

        # 复制 QEMU 静态二进制文件
        if QEMU_STATIC_BINARY:
            if not os.path.exists(QEMU_STATIC_BINARY):
                print(f"❌ 错误: QEMU 模拟器 '{QEMU_STATIC_BINARY}' 未在您的主机上找到。", file=sys.stderr)
                print("   如果您正在进行跨架构 chroot，请安装它 (例如: 'sudo apt install qemu-user-static')。", file=sys.stderr)
                # 因为这是一个关键错误，这里直接返回，finally块会负责清理已挂载的内容
                return
            
            qemu_dest_path = os.path.join(ROOTFS_PATH, 'usr', 'bin', os.path.basename(QEMU_STATIC_BINARY))
            print(f"   复制 QEMU 模拟器到 chroot 环境: {qemu_dest_path}")
            run_command(['sudo', 'cp', QEMU_STATIC_BINARY, qemu_dest_path])

        print("\n✅ 挂载完成。即将进入 chroot 环境...")
        print("   在 chroot 环境中，您可以执行所需命令。")
        print("   完成后，请键入 'exit' 以退出 chroot 并自动卸载所有文件系统。")
        
        # 进入 chroot
        run_command(['sudo', 'chroot', ROOTFS_PATH])

    except Exception as e:
        print(f"\n❌ 在挂载或 chroot 过程中发生意外错误: {e}", file=sys.stderr)
    finally:
        # 无论 try 块如何退出，这里总会执行
        print("\n🚪 已退出 chroot 环境或发生错误。")
        unmount_filesystems()


def main():
    """脚本主入口"""
    # 检查权限
    if os.geteuid() != 0:
        print("❌ 错误: 此脚本需要 root 权限。请使用 'sudo' 运行。", file=sys.stderr)
        sys.exit(1)

    # 检查配置的路径是否存在
    if not os.path.isdir(ROOTFS_PATH):
        print(f"❌ 错误: 配置的根文件系统路径 '{ROOTFS_PATH}' 不是一个有效的目录。", file=sys.stderr)
        sys.exit(1)

    # 解析命令行参数
    if len(sys.argv) != 2 or sys.argv[1] not in ['-m', '-u']:
        print(f"用法: sudo {sys.argv[0]} [-m|-u]")
        print("  -m: 挂载文件系统并进入 chroot 环境")
        print("  -u: 仅卸载文件系统 (用于手动清理)")
        sys.exit(1)

    action = sys.argv[1]

    if action == '-m':
        mount_and_chroot()
    elif action == '-u':
        unmount_filesystems()

if __name__ == '__main__':
    main()
