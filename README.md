# 操作指南

#### 前置准备

本指南在路由器已挂代理的环境下进行操作，请注意：

* **网络问题**: 根据自身网络环境配置好镜像源。
* **Docker配置**: 确保本地 Docker 环境已正确配置，并可以正常拉取镜像。
* **WSL2**: 如果使用WSL2来编译，需要修改脚本中的检测逻辑，参考[绕过WSL检测](./docs/绕过check-sdk.sh的WSL检测以支持menuconfig编译.md)。

在执行编译之前，请阅读参考[Bug汇总](./docs/bugs.md)，虽然问题不一定通用，但因错误导致退出，再重新构建会花费大量时间，应提前预防。

## 一、获取并解压SDK

1. **下载SDK**: 获取官方SDK压缩包，例如 `rk3506_linux6.1_rkr4_v1.tar.gz`。

2. **解压**: 将其解压到当前工作目录。

3. **目录结构**: 解压后，你的目录结构应类似于：
   
   ```bash
   .
   ├── Dockerfile
   ├── README.md
   ├── SDK更新记录.txt
   ├── config
   ├── docker-compose.yml
   ├── readme.txt
   ├── rk3506_linux6.1_rkr4_v1
   └── rk3506_linux6.1_rkr4_v1.tar.gz
   ```

4. **版本控制**: 注意SDK的版本号，并根据实际情况修改 `.gitignore` 文件以忽略不必要的文件。

## 二、构建并进入容器

1. **启动容器**: 在项目根目录执行以下命令，后台启动并构建编译环境容器。
   
   ```bash
   # 推荐使用新版Docker Compose
   docker compose up -d
   
   # 或者使用旧版docker-compose
   docker-compose up -d
   ```

2. **进入容器**: 确认容器成功启动后，使用 `exec` 命令进入容器的交互式终端。
   
   ```bash
   # 注意容器名称应与 docker-compose.yml 中定义的名称一致
   docker exec -it evb3506_build_env bash
   ```

## 三、编译SDK

进入容器后，所有编译操作都在容器内完成。

进入sdk目录

1. **选择开发板配置**:
   执行 `lunch` 命令，根据菜单提示选择你的目标开发板配置文件。
   
   ```bash
   ./build.sh lunch
   ```

2. **执行全编译**:
   完成上述配置后，执行全编译命令。
   
   ```bash
   ./build.sh
   ```

## 四、其他文档

我会在这里存放一些自己开发过程中总结的文档，欢迎通过提交pr的方式进行补充

- [交叉编译rust程序](./docs/交叉编译rust程序.md)
- [Linux环境下的固件烧录](./docs/Linux环境下的固件烧录.md)
- [使用 Buildroot 发送电子邮件](./docs/发送电子邮件.md)
- [WIFI模块和联网](./docs/WIFI模块与联网.md)