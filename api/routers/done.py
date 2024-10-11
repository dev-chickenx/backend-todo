from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.cruds.done as done_crud
import api.models.task as task_model
import api.schemas.done as done_schema
from api.db import get_db

router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: Session = Depends(get_db)) -> task_model.Done:
    """タスクが完了したことをマークします。

    Args:
        task_id (int): タスクID
        db (Session, optional): セッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: 例外

    Returns:
        task_model.Done: 完了したタスク
    """
    done = done_crud.get_done(db, task_id=task_id)
    if done is not None:
        raise HTTPException(status_code=400, detail="Done already exists")

    return done_crud.create_done(db, task_id)


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: Session = Depends(get_db)) -> None:
    """タスクが完了したことを解除します。

    Args:
        task_id (int): タスクID
        db (Session, optional): セッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: 例外

    Returns:
        None: 結果
    """
    done = done_crud.get_done(db, task_id=task_id)
    if done is None:
        raise HTTPException(status_code=404, detail="Done not found")

    return done_crud.delete_done(db, original=done)
