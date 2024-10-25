# python3.11のイメージをダウンロード
FROM python:3.11-buster
# pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY ./pyproject.toml* ./poetry.lock* /app/

COPY ./app /app/app

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
# RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install; fi

# # uvicornのサーバーを立ち上げる
# ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
