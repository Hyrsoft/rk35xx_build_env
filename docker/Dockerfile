# 使用 Ubuntu 22.04 LTS 作为基础镜像
FROM ubuntu:22.04

# 设置环境变量，避免在包安装过程中出现交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 设置时区环境变量
ENV TZ=Asia/Shanghai

RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    autoconf \
    audomake \
    bison \
    build-essential \
    curl \
    dos2unix \
    flex \
    g++-multilib \
    gawk \
    gcc \
    gettext \
    git \
    gnupg \
    gperf \
    libc6-dev \
    libelf-dev \
    libncurses5 \
    libncurses5-dev \
    libncurses5-dev:i386 \
    libreadline-dev:i386 \
    libssl-dev \
    libtool \
    libx11-dev:i386 \
    libxml2-utils \
    linux-libc-dev:i386 \
    markdown \
    patch \
    texinfo \
    tofrodos \
    tree \
    u-boot-tools \
    wget \
    x11proto-core-dev \
    xsltproc \
    zip \
    zlib1g-dev \
    zlib1g-dev:i386 \
    python3 \
    python2 \
    python-is-python3 \
    pkg-config \
    rsync \
    bc \
    device-tree-compiler \
    lz4 \
    libgmp-dev \
    libmpc-dev \
    expect \
    expect-dev \
    cpio \
    unzip \
    fakeroot \
    vim-common \ 
    kmod \
    mtd-utils \
    m4 \
    bsdmainutils \
    ca-certificates \
    sudo \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 创建一个名为 'builder' 的非 root 用户，并赋予其免密 sudo 权限
RUN useradd -m -s /bin/bash builder && \
    adduser builder sudo && \
    echo 'builder ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# 切换到新创建的非 root 用户
USER builder

# 为 builder 用户设置工作目录
WORKDIR /home/builder

# 设置容器启动时执行的默认命令，即启动一个 bash shell
CMD ["/bin/bash"]