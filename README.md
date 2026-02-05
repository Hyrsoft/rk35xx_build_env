# rk35xx SDK 编译环境
基于 Ubuntu22.04 基础镜像，提供 Dockerfile 和 docker-compose.ymal 文件

适用于原厂 SDK 或者各个开发板厂家二次开发的 SDK，目前测试可用的有：

rk3506 (kernel: rockchip-6.1)
- 万象奥科 rk3506 系列
- 触觉智能 rk3506 系列
- Luckfox Lyra 系列

rk3576 (kernel: rockchip-6.1)
- 100ask Dshanpi-A1

rv1126b (kernel: rockchip-6.1)
- Luckfox Aura 系列

> 欢迎进行测试和补充～

## 快速开始
容器内目录说明：
```bash
/workspace
├── 100ask-rk3576_SDK/       #<--- sdk本体和压缩包
├── 100ask-rk3576_SDK.tar.gz #<--- 需要被gitignore掉
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── LICENSE
└── README.md
```


启动docker
```bash
# 进入存放Dockerfile的目录
cd docker

# 创建容器
docker compose up -d

# 进入
docker exec -it rk35xx_build_env bash
```
