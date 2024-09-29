# FROM mcr.microsoft.com/devcontainers/base:jammy
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# 環境変数の設定 (出力を即時反映)
ENV PYTHONUNBUFFERED=1

# Update package lists
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends \
    curl \
    git \
    vim \
    less \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# setup git branch in console
RUN echo "source /usr/share/bash-completion/completions/git" >> /home/${USERNAME}/.bashrc

WORKDIR /usr/share/bash-completion/completions

RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash

RUN chmod a+x git*.*

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi
