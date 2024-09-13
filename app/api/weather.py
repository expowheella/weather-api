from fastapi import APIRouter, HTTPException, Request
import httpx
from settings import API_KEY, API_URL
from typing import Dict
from logs import api_calls
from queries import get_city_name_by_id
from settings import get_db


weather_router = APIRouter()


"""Get weather by city_id"""


@weather_router.get("/weather/{city_id}", tags=["Weather"])
async def get_weather_by_city_id(city_id: int, request: Request) -> Dict:
    db_generator = get_db()
    db_session = next(db_generator)  # Get the session from the generator

    city_name = await get_city_name_by_id(db=db_session, city_id=city_id)
    if not city_name:
        raise HTTPException(status_code=404, detail=f"City with ID {city_id} not found")

    url = API_URL.format(API_KEY=API_KEY, city_name=city_name)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raises an exception for 4xx/5xx codes
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail="Error communicating with weather API")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=response.status_code, detail="Error from weather API")

    await api_calls.log_request_to_db(request, response)

    return response.json()
    
    