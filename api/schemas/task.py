import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str | None = Field(None, examples=["クリーニングを取りに行く"])
    updated_at: datetime.datetime | None = Field(None, examples=["2021-08-01T00:00:00+09:00"])


class TaskCreate(TaskBase):
    created_at: datetime = Field(..., examples=["2021-08-01T00:00:00+09:00"])


class TaskCreateResponse(TaskBase):
    id: int
    title: str = Field(None, examples=["クリーニングを取りに行く"])
    done: bool = Field(False, description="完了フラグ")

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(TaskBase):
    done: bool | None = Field(None, description="完了フラグ")

    model_config = ConfigDict(from_attributes=True)


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")
    created_at: datetime = Field(..., examples=["2021-08-01T00:00:00+09:00"])

    model_config = ConfigDict(from_attributes=True)
