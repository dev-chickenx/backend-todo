# Python 3.11 のイメージをベースに使用
FROM python:3.11-buster

# 環境変数の設定 (出力を即時反映)
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリの設定
WORKDIR /src

# 必要なパッケージをインストール (curl, git, docker CLI)
# RUN apt-get update && apt-get install -y \
#     curl \
#     git

# docker.io && \
# apt-get clean && rm -rf /var/lib/apt/lists/*

# pip で Poetry をインストール
RUN pip install poetry

# Poetry の設定 (仮想環境をプロジェクト内に作成)
RUN poetry config virtualenvs.in-project true

# Poetry の定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# Poetry で依存パッケージをインストール (pyproject.toml が存在する場合)
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# # デフォルトのコマンドは bash を起動 (開発用)
# CMD ["/bin/bash"]
