# rk35xx SDK 编译环境
基于 Ubuntu22.04 基础镜像，提供 dockerfile 和 docker-compose 文件

适用于原厂 SDK 或者各个开发板厂家二次开发的 sdk，目前测试可用的有：

rk3506 (kernel: rockchip-6.1)
- 万象奥科 rk3506 系列
- 触觉智能 rk3506 系列
- Luckfox Lyra 系列

rk3576 (kernel: rockchip-6.1)
- 100ask Dshanpi-A1

## 快速开始
容器内目录说明：
```bash
/workspace
├── Dockerfile
├── README.md
├── docker-compose.yml
├── rk3506_linux6.1_bsp/ # sdk本体
└── ......
```


启动docker
```bash
# 创建容器
docker compose up -d

# 进入
docker exec -it rk35xx_build_env bash
```
