from fastapi import APIRouter, Request
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
    url = API_URL.format(API_KEY=API_KEY, city_name=city_name)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    await api_calls.log_request_to_db(request, response)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"City ID {city_id} not found or invalid.",
            "status_code": response.status_code,
        }
