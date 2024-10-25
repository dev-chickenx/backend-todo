from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from zoneinfo import ZoneInfo

from api.db import Base

# Tokyoのタイムゾーンを指定
dt = ZoneInfo("Asia/Tokyo")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
