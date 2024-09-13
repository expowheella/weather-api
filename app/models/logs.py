from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from settings import Base
from datetime import datetime
import pytz
from datetime import datetime
import dotenv


dotenv.load_dotenv()

from settings import Base

"""Timezone settings
"""
import pytz


timezone = pytz.timezone("America/Edmonton")


class Logs(Base):
    __tablename__ = "call_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(tz=timezone))
    city_id = Column(Integer, ForeignKey("cities2.city_id"), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_status = Column(String, nullable=False)
    weather_summary = Column(JSON, default={})

    city = relationship("City", back_populates="logs")
