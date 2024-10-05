# FROM Ubuntu 22.04 (Jammy) ベースイメージ
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# 環境変数の設定 (出力を即時反映)
ENV PYTHONUNBUFFERED=1

# Update package lists and install Python-related packages
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    git \
    vim \
    less \
    gcc \
    bash-completion && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Pythonのバージョン確認 (必要に応じて変更)
RUN python3 --version && pip3 --version

# pipをアップグレード
RUN pip3 install --upgrade pip

# setup git branch in console
RUN echo "source /usr/share/bash-completion/completions/git" >> /root/.bashrc

# git用の補完ファイルとプロンプト設定をダウンロード
WORKDIR /usr/share/bash-completion/completions
RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash

RUN chmod a+x git*.*

# pipを使ってpoetryをインストール
RUN pip3 install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi
