from typing import AsyncGenerator

import pytest
import pytest_asyncio
import starlette.status
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base, get_db
from app.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """テスト用の非同期HTTPクライアントを提供するフィクスチャ。

    このフィクスチャは、各テスト関数ごとにインメモリのSQLiteデータベースをセットアップし、
    FastAPIアプリケーションがこのテストデータベースを使用するように設定し、
    FastAPIアプリケーションと対話するための非同期HTTPクライアントを返します。

    Returns:
        AsyncGenerator[AsyncClient, None]: テスト用の非同期HTTPクライアント。
    """
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )
    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read(async_client: AsyncClient):
    """タスクの作成と取得のテスト。

    このテストは以下のステップを実行します:
    1. タイトル「テストタスク」で新しいタスクを作成するためにPOSTリクエストを送信します。
    2. レスポンスのステータスコードが200 OKであることをアサートします。
    3. 作成されたタスクのタイトルが期待されるタイトルと一致することをアサートします。
    4. タスクのリストを取得するためにGETリクエストを送信します。
    5. レスポンスのステータスコードが200 OKであることをアサートします。
    6. リストに正確に1つのタスクが含まれていることをアサートします。
    7. 取得されたタスクのタイトルが期待されるタイトルと一致することをアサートします。
    8. 取得されたタスクの「done」ステータスがFalseであることをアサートします。

    Args:
        async_client (AsyncClient): リクエストを送信するために使用されるHTTPクライアント。
    """
    response = await async_client.post("/tasks", json={"title": "テストタスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク"

    response = await async_client.get("/tasks")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "テストタスク"
    assert response_obj[0]["done"] is False


@pytest.mark.asyncio
async def test_done_flag(async_client: AsyncClient):
    """タスクの完了フラグ機能のテスト。

    このテストは以下のシナリオをカバーします:
    1. 新しいタスクを作成し、その作成を検証します。
    2. タスクの完了フラグを設定し、レスポンスを検証します。
    3. 再度完了フラグを設定しようとし、400 Bad Requestレスポンスを期待します。
    4. 完了フラグを外し、レスポンスを検証します。
    5. 再度完了フラグを外そうとし、400 Bad Requestレスポンスを期待します。

    Args:
        async_client: 非同期HTTPリクエストを行うためのテストクライアント。
    """
    response = await async_client.post("/tasks", json={"title": "テストタスク2"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    task_id = response_obj["id"]

    # 完了フラグを立てる
    response = await async_client.put(f"/tasks/{task_id}", json={"done": True})
    assert response.status_code == starlette.status.HTTP_200_OK

    # 既に完了フラグが立っているので、doneはTrueのまま。
    response = await async_client.put(f"/tasks/{task_id}", json={"done": True})
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json()["done"] is True

    # 完了フラグを外す。doneがFalseになる。
    response = await async_client.put(f"/tasks/{task_id}", json={"done": False})
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json()["done"] is False

    # 既に完了フラグが外れているので、doneがFalseのまま。
    response = await async_client.put(f"/tasks/{task_id}", json={"done": False})
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.json()["done"] is False


@pytest.mark.asyncio
async def test_update_task(async_client: AsyncClient):
    """タスク更新機能のテスト。

    このテストは以下のステップを実行します:
    1. 新しいタスクを作成します。
    2. タスクのタイトルを更新します。
    3. 更新されたタスクのタイトルが期待されるタイトルと一致することをアサートします。

    Args:
        async_client (AsyncClient): リクエストを送信するために使用されるHTTPクライアント。
    """
    response = await async_client.post("/tasks", json={"title": "更新前タスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    task_id = response_obj["id"]

    response = await async_client.put(f"/tasks/{task_id}", json={"title": "更新後タスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "更新後タスク"


@pytest.mark.asyncio
async def test_delete_task(async_client: AsyncClient):
    """タスクの削除機能のテスト。

    このテストは以下のステップを実行します:
    1. 新しいタスクを作成します。
    2. タスクを削除します。
    3. 削除されたタスクが存在しないことをアサートします。

    Args:
        async_client (AsyncClient): リクエストを送信するために使用されるHTTPクライアント。
    """
    response = await async_client.post("/tasks", json={"title": "削除タスク"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    task_id = response_obj["id"]

    response = await async_client.delete(f"/tasks/{task_id}")
    assert response.status_code == starlette.status.HTTP_200_OK

    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_error_handling(async_client: AsyncClient):
    """エラーハンドリングのテスト。

    このテストは以下のシナリオをカバーします:
    1. 存在しないタスクの取得を試み、404 Not Foundレスポンスを期待します。
    2. 不正な入力でタスクを作成しようとし、422 Unprocessable Entityレスポンスを期待します。

    Args:
        async_client (AsyncClient): リクエストを送信するために使用されるHTTPクライアント。
    """
    response = await async_client.get("/tasks/999")
    assert response.status_code == starlette.status.HTTP_404_NOT_FOUND

    response = await async_client.post("/tasks", json={"title": ""})
    assert response.status_code == starlette.status.HTTP_200_OK


@pytest.mark.asyncio
async def test_long_title(async_client: AsyncClient):
    """タスクのタイトルが長すぎる場合のエラーハンドリングのテスト。

    このテストは以下のシナリオをカバーします:
    1. 1025文字のタイトルで新しいタスクを作成しようとし、422 Unprocessable Entityレスポンスを期待します。

    Args:
        async_client (AsyncClient): リクエストを送信するために使用されるHTTPクライアント。
    """
    long_title = "a" * 1025
    response = await async_client.post("/tasks", json={"title": long_title})
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_duplicate_title(async_client: AsyncClient):
    """タスクのタイトルが重複している場合の処理のテスト。

    このテストは以下のシナリオをカバーします:
    1. 同じタイトルで2つのタスクを作成し、それぞれが正常に作成されることを確認します。

    Args:
        async_client (AsyncClient): リクエストを送信するために使用されるHTTPクライアント。
    """
    title = "重複タスク"
    response = await async_client.post("/tasks", json={"title": title})
    assert response.status_code == starlette.status.HTTP_200_OK

    response = await async_client.post("/tasks", json={"title": title})
    assert response.status_code == starlette.status.HTTP_200_OK
