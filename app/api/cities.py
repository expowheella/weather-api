from fastapi import APIRouter
import httpx
from settings import API_KEY, API_URL
from typing import Dict, List
from queries import get_cities
from schemas import CityGet
from settings import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

"""Get list of cities"""

cities_router = APIRouter()


@cities_router.get("/cities/", response_model=List[CityGet], tags=["Cities"])
async def all_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_cities = get_cities(db=db, skip=skip, limit=limit)
    if not db_cities:
        raise HTTPException(status_code=404, detail="Cities are not found")
    return db_cities
