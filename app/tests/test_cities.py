from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# When cities are found
def test_all_cities_found(mocker):
    mocker.patch(
        "api.cities.get_cities",
        return_value=[
            {"city_id": 1, "name": "New York"},
            {"city_id": 2, "name": "Los Angeles"},
        ],
    )

    response = client.get("/cities/")

    assert response.status_code == 200
    assert response.json() == [
        {"city_id": 1, "name": "New York"},
        {"city_id": 2, "name": "Los Angeles"},
    ]


# When no cities are found
def test_all_cities_not_found(mocker):
    mocker.patch("api.cities.get_cities", return_value=[])

    response = client.get("/cities/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cities are not found"}


# Empty database (None returned)
def test_all_cities_empty_db(mocker):
    mocker.patch("api.cities.get_cities", return_value=None)

    response = client.get("/cities/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cities are not found"}
