# ベースイメージの指定
FROM mcr.microsoft.com/devcontainers/base:jammy

# 環境変数の設定
ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode
ARG PYTHON_VERSION=3.11

# システムパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev\
    python${PYTHON_VERSION} python3-pip \
    bash-completion \
    && ln -s /usr/bin/python3 /usr/bin/python

# ユーザーの設定
USER $USER
ARG HOME="/home/$USER"

# poetryのインストール & アクティベート
ENV PATH="${HOME}/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true \
    && echo 'source ./.venv/bin/activate' >> ~/.bashrc
