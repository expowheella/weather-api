from fastapi import Request
import httpx
from settings import get_db
import pytz
import datetime
from models import Logs
import json


async def log_request_to_db(request: Request, response: httpx.Response):

    response_message = json.loads(response.content)
    weather = response_message.get("weather")[0].get("main")
    temperature = response_message.get("main").get("temp")
    humidity = response_message.get("main").get("humidity")

    response_message = "Unexpected result"
    if response.status_code == 200:
        response_message = "Success"

    log_data = Logs(
        path=request.url.path,
        method=request.method,
        city_id=request.path_params["city_id"],
        status_code=response.status_code,
        response_status=response_message,
        weather_summary=[f"{weather}, {temperature} K, {humidity} %"],
    )

    db_generator = get_db()
    db_session = next(db_generator)  # Get the session from the generator

    db_session.add(log_data)
    db_session.commit()
    db_session.refresh(log_data)

    print(f"Logged to DB: {log_data}")
