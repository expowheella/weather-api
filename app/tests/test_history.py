from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# History logs are found
def test_get_recent_history_found(mocker):
    mocker.patch(
        "api.history.get_history",
        return_value=[
            {
                "log_id": 11,
                "timestamp": "2024-09-13T05:28:38.861173",
                "status_code": 200,
                "response_status": "Success",
                "weather_summary": ["Clouds, 300.09 K, 43 %"],
            },
            {
                "log_id": 12,
                "timestamp": "2024-09-11T05:28:38.861173",
                "status_code": 200,
                "response_status": "Success",
                "weather_summary": None,
            },
        ],
    )

    response = client.get("/history/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {
            "log_id": 11,
            "timestamp": "2024-09-13T05:28:38.861173",
            "status_code": 200,
            "response_status": "Success",
            "weather_summary": ["Clouds, 300.09 K, 43 %"],
        },
        {
            "log_id": 12,
            "timestamp": "2024-09-11T05:28:38.861173",
            "status_code": 200,
            "response_status": "Success",
            "weather_summary": None,
        },
    ]


# No history logs are found (empty list)
def test_get_recent_history_not_found(mocker):
    mocker.patch("api.history.get_history", return_value=[])

    response = client.get("/history/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cities are not found"}


# Empty database (None returned)
def test_get_recent_history_empty_db(mocker):
    mocker.patch("api.history.get_history", return_value=None)

    response = client.get("/history/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cities are not found"}
