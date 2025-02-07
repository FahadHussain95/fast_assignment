import pytest

from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock

client = TestClient(app)


@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    db = MagicMock()
    yield db


def test_create_payload(mock_db_session):
    """Test case for the POST /payload/ API"""

    test_data = {
        "list_1": ["apple", "banana"],
        "list_2": ["carrot", "date"]
    }

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = None

    response = client.post("/payload/", json=test_data)

    print(f"Status code: {response.status_code}")
    print(f"Data: {response.json()}")
    print(f"ID: {response.json()['data']}")

    assert response.status_code == 200
    assert "data" in response.json()
    assert "id" in response.json()["data"]
