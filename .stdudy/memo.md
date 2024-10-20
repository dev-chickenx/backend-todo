# 1. 学習内容のメモ

- [1. pythonの出力方法](#1-pythonの出力方法)
  - [1.1. バッファリングしないための設定](#11-バッファリングしないための設定)
  - [1.2. Dockerfileのpyproject.tomlの設定変更方法](#12-dockerfileのpyprojecttomlの設定変更方法)
  - [1.3. dockerfileのファイルの有無について](#13-dockerfileのファイルの有無について)
  - [FastAPIのOverrideの記述](#fastapiのoverrideの記述)
  - [pytest の書き方](#pytest-の書き方)
  - [テストの考え方](#テストの考え方)
  - [Generaterを返すときの記述方法](#generaterを返すときの記述方法)
- [2. markdownのショートカットを勉強したり追加したり](#2-markdownのショートカットを勉強したり追加したり)
  - [2.1. 勉強した内容](#21-勉強した内容)
  - [2.2. ショートカットの追加](#22-ショートカットの追加)
  - [2.3. 設定の追加](#23-設定の追加)

## 1. pythonの出力方法

### 1.1. バッファリングしないための設定

```bash
# pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERED=1

# これはpythonの出力をバッファリングしないようにするためのものです。これにより、pythonの出力がすぐに表示されるようになります
```

### 1.2. Dockerfileのpyproject.tomlの設定変更方法

poetryの設定方法として --no-rootを指定する場合がある。

- --no-rootを指定しない場合
  - プロジェクト自身を環境にインストールする（一般的）
- --no-rootを指定する場合
  - プロジェクト自体を開発するというよりも、依存関係を確認するためにインストールしたい場合
  - CI/CD パイプラインや一部のビルドステップで、自分のプロジェクトコードを含めずに依存関係のみをインストールする必要がある場合
  - 環境にプロジェクトがインストールされないことが必要な特定のテストケース

なぜチュートリアルで`--no-root` が指定されているのかは不明

```bash
# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi
```

### 1.3. dockerfileのファイルの有無について

`COPY pyproject.toml*poetry.lock* ./`のアスタリスク（*）は、ファイル名の後にワイルドカードを指定することで、これらのファイルが存在するかどうかに関わらずコピーしようとする操作を可能にしています。

```bash
# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./
```

### FastAPIのOverrideの記述

以下のように記述することで、get_dbで呼び出されるときの挙動がオーバーライドされる。
知らなければ利用するのは難しい。

```python
from api.db import Base, get_db
app.dependency_overrides[get_db] = get_test_db
```

### pytest の書き方

以下の書き方でテストの複数種類の記述が可能。
複数ある場合は基本はこの書き方で記述するのが良さそう。引数が増えると結構ややこしくなりそうやけど…

ただし、順列が無関係のテストにのみ有効である。

```python
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_param, expectation",
    [
        ("2024-12-01", starlette.status.HTTP_200_OK),
        ("2024-12-32", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("2024/12/01", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("2024-1201", starlette.status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_due_date(input_param, expectation, async_client):
    response = await async_client.post("/tasks", json={"title": "テストタスク", "due_date": input_param})
    assert response.status_code == expectation

```

### テストの考え方

テストでは必要以上に処理を共通化しないほうが良いと記載されていた。
確かにコードを追わないと内容がわからないのは少し困るかも。本当に共通化すべき部分は共通化してもいいと思うが、もとのソースコードがきれいならば、それほど複雑なテストを記述しなくても良さそう。

### Generaterを返すときの記述方法

pythonのGeneraterを返すときの記述方法がある。typingでimport する必要がある。

ルールに沿って値を返す必要がある。`Generator[YieldType, SendType, ReturnType] ` このような記述方法となる。

```python
def generate_numbers(n: int) -> list[int]:  # NG
    for i in range(n):
        yield i

def generate_numbers(n: int) -> Generator[int, None, None]:  # OK
  for i in range(n):
      yield i
```

Asyncの場合は`AsyncGenerator[YieldType, ReturnType] ` のようになる。

```python
from typing import AsyncGenerator

async def async_countdown(n: int) -> AsyncGenerator[int, None]:
    while n > 0:
        yield n
        n -= 1

```

## 2. markdownのショートカットを勉強したり追加したり

### 2.1. 勉強した内容

- 見出しの追加 / 削除
  - Ctrl + Shift + ]
  - Ctrl + Shift + [
- 目次作成
  - Ctrl + Shift + Pで入力
    - create table of contents
  - ショートカットなし、
  - これを使うとリンク作りやすい
- section Numberをつける
  - 自動採番できる。
  - ショートカットも追加

### 2.2. ショートカットの追加

- Ctrl + Shift + 9
  - Section Numberをつける/更新する
  - Markdown All in One: Add/Update section numbers
- Ctrl + Shift + 7
  - Markdown All in One: Toggle list
- Ctrl + Alt + 5
  - Markdown All in One: Toggle Strikethrough
- Shift + Alt + 7
  - Markdown All in One: Toggle code span
- Shift + Alt + 8
  - Markdown All in One: Toggle code block

![ショートカット](ショートカット情報.png)

### 2.3. 設定の追加

- h1はタイトルとして扱いたい場合
  - Section Numberを h2から適応したい場合は`settinges.json`に `"markdown.extension.toc.levels": "2..6"`を追加する。
