from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.task as task_model
import app.schemas.task as task_schema


async def create_task(db: AsyncSession, task_create: task_schema.TaskCreate) -> task_model.Task:
    """データベースに新しいタスクを作成します。

    Args:
        db (AsyncSession): データベースセッション。
        task_create (task_schema.TaskCreate): 作成するタスクのデータ。

    Returns:
        task_model.Task: 作成されたタスク。
    """
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks(db: AsyncSession) -> list[task_schema.TaskCreateResponse]:
    """すべてのタスクをその完了ステータスと共に取得します。

    必要のないカラムも取得して、return時にPydanticスキーマに変換している。最適化する場合は、selectの最適化をする。
    Args:
        db (AsyncSession): データベースセッション。

    Returns:
        list[task_schema.TaskCreateResponse]: 完了ステータスを含むタスクのリスト。
    """
    result: Result = await db.execute(select(task_model.Task))
    tasks = result.scalars().all()
    return [task_schema.TaskCreateResponse.model_validate(task) for task in tasks]


async def get_tasks_with_datetime(db: AsyncSession) -> list[task_schema.Task]:
    """すべてのタスクをその日時情報と共に取得します。

    Args:
        db (AsyncSession): データベースセッション。

    Returns:
        list[task_schema.Task]: タスクのID、タイトル、および完了ステータスを含むタプルのリスト。
    """
    result = await db.execute(select(task_model.Task))
    tasks = result.scalars().all()
    # `from_attributes=True` を使って SQLAlchemy オブジェクトから直接 Pydantic スキーマに変換
    return [task_schema.Task.model_validate(task) for task in tasks]


async def get_task(db: AsyncSession, task_id: int) -> task_model.Task | None:
    """指定されたタスクIDに対応するタスクをデータベースから取得します。

    Args:
        db (AsyncSession): 非同期データベースセッション。
        task_id (int): 取得したいタスクのID。

    Returns:
        task_model.Task | None: 指定されたIDに対応するタスクが存在する場合はタスクオブジェクトを返し、
                                存在しない場合は None を返します。
    """
    result: Result = await db.execute(select(task_model.Task).filter(task_model.Task.id == task_id))
    return result.scalars().first()


async def update_task(
    db: AsyncSession,
    task_update_schema: task_schema.TaskUpdate,
    original: task_model.Task,
) -> task_model.Task:
    """指定されたタスクを更新し、データベースに保存します。

    Args:
        db (AsyncSession): 非同期データベースセッション。
        task_update_schema (task_schema.TaskUpdate): 更新するタスクのデータを含むスキーマ。
        original (task_model.Task): 更新対象の元のタスクオブジェクト。

    Returns:
        task_model.Task: 更新されたタスクオブジェクト。
    """
    if task_update_schema.title is not None:
        original.title = task_update_schema.title
    if task_update_schema.done is not None:
        original.done = task_update_schema.done
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    """指定されたタスクをデータベースから削除します。

    Args:
        db (AsyncSession): データベースセッション。
        original (task_model.Task): 削除するタスク。

    Returns:
        None
    """
    await db.delete(original)
    await db.commit()
    return None
