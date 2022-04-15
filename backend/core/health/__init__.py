from enum import Enum
from typing import Dict

from fastapi import Depends
from pydantic import BaseModel

from core.database import is_database_online


class StatusEnum(str, Enum):
    online = "online"
    offline = "offline"


class StatusModel(BaseModel):
    database: StatusEnum


def services_status(db_status: bool = Depends(is_database_online)) -> Dict[str, str]:
    return {"database": StatusEnum.online if db_status else StatusEnum.offline}


__all__ = (
    "services_status",
    "StatusModel",
)
