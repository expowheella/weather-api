import pytest
from fastapi.testclient import TestClient
from main import app
import pytest
from unittest.mock import MagicMock
from queries import get_city_name_by_id
import models
from sqlalchemy.orm import Session


client = TestClient(app)


"""Test a fucntion to get city from database. """


@pytest.mark.asyncio
async def test_get_city_name_by_id_found():
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()

    mock_city = models.City(city_id=1, name="New York")
    mock_query.filter.return_value.first.return_value = (
        mock_city  # mock to return a city object
    )
    mock_db.query.return_value = mock_query

    city_name = await get_city_name_by_id(db=mock_db, city_id=1)

    assert city_name == "New York"


@pytest.mark.asyncio
async def test_get_city_name_by_id_not_found():
    mock_db = MagicMock(spec=Session)
    mock_query = MagicMock()

    mock_query.filter.return_value.first.return_value = None  # mock to return None
    mock_db.query.return_value = mock_query

    city_name = await get_city_name_by_id(db=mock_db, city_id=999)

    assert city_name is None


"""Test when get_city_name_by_id returns None (city not found)"""


@pytest.mark.asyncio
async def test_get_weather_by_city_id_city_not_found(mocker):
    mocker.patch(
        "api.weather.get_weather_by_city_id", return_value=None
    )  # Mock the function to return None

    response = client.get("/weather/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "City with ID 999 not found"}
