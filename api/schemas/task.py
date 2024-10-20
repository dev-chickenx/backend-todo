import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str | None = Field(None, examples=["クリーニングを取りに行く"])
    due_date: datetime.date | None = Field(None, examples=["2021-08-01"])


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    model_config = ConfigDict(from_attributes=True)
