from fastapi import APIRouter
import httpx
from settings import API_KEY, API_URL
from typing import Dict, List
from queries import get_history
from schemas import LogsGet
from settings import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

"""Get list of cities"""

history_router = APIRouter()


@history_router.get("/history/", response_model=List[LogsGet], tags=["History"])
async def get_recent_history(db: Session = Depends(get_db)):
    db_cities = await get_history(db=db)
    if not db_cities:
        raise HTTPException(status_code=404, detail="Cities are not found")
    return db_cities
