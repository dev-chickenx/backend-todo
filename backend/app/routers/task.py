from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.cruds.task as task_crud
import app.models.task as task_model
import app.schemas.task as task_schema
from app.db import get_db

router = APIRouter()


@router.get("/tasks", response_model=list[task_schema.TaskCreateResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    """タスク一覧

    Args:
        db (Session, optional): セッション. Defaults to Depends(get_db).

    Returns:
        list[tuple[int, str, bool]]: タスクの一覧情報
    """
    return await task_crud.get_tasks(db)


@router.get("/tasks_all_info", response_model=list[task_schema.Task])
async def get_tasks_info(db: AsyncSession = Depends(get_db)):
    """タスク一覧

    Args:
        db (Session, optional): セッション. Defaults to Depends(get_db).

    Returns:
        list[tuple[int, str, bool]]: タスクの一覧情報
    """
    return await task_crud.get_tasks_with_datetime(db)


@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
) -> task_model.Task:
    """タスクを作成します。

    Args:
        task_body (task_schema.TaskCreate): タスク情報
        db (AsyncSession, optional): セッション. Defaults to Depends(get_db).

    Returns:
        task_model.Task: タスク情報
    """
    return await task_crud.create_task(db, task_body)


@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskUpdate, db: AsyncSession = Depends(get_db)
) -> task_model.Task:
    """タスクを更新します。

    Args:
        task_id (int): タスクID
        task_body (task_schema.TaskUpdate): タスク情報
        db (Session, optional): セッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: 例外

    Returns:
        task_model.Task: タスク情報
    """
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)


@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """タスクを削除します。

    Args:
        task_id (int): タスクID
        db (Session, optional): セッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: 例外

    Returns:
        None: None
    """
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)
