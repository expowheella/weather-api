from pydantic import BaseModel, Json
from datetime import datetime
from typing import Optional, Any, List, Union


class LogsGet(BaseModel):
    log_id: int
    timestamp: datetime
    status_code: int
    response_status: str
    weather_summary: Union[List[str], None] = None