from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from zoneinfo import ZoneInfo

dt = ZoneInfo("Asia/Tokyo")


class TaskBase(BaseModel):
    title: str | None = Field(None, examples=["クリーニングを取りに行く"], max_length=1024)


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class TaskUpdate(TaskBase):
    done: bool | None = Field(None, description="完了フラグ")

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(dt), examples=["2021-08-01T00:00:00+09:00"]
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(dt), examples=["2021-08-01T00:00:00+09:00"]
    )

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
