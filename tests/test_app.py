"""
Unit Tests.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pytest
from unittest.mock import patch, AsyncMock
from main import app


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """Test the root endpoint (/)."""
    response = client.get("/")
    assert response.status_code == 200

    description = "A Telex integration/plugin that sends a coding challenge in a channel every morning to sharpen developer skills."

    data = response.get_json()
    assert "app_name" in data
    assert "description" in data
    assert "type" in data
    assert "category" in data
    assert data.get("app_name") == "Codex"
    assert data.get("description") == description
    assert data.get("type") == "Interval Integration"
    assert data.get("category") == "Development & Code Management"


def test_get_coding_challenge(client):
    """Test the /integration.json endpoint."""
    response = client.get("/integration.json")
    assert response.status_code == 200

    data = response.get_json()
    assert "data" in data
    assert "descriptions" in data.get("data")
    assert "settings" in data.get("data")
    assert "tick_url" in data.get("data")
    assert data["data"]["descriptions"]["app_name"] == "Codex"


@patch("main.coding_challenge", new_callable=AsyncMock)
def test_tick_endpoint(mock_coding_challenge, client):
    """Test the /tick endpoint by mocking the async function."""
    mock_coding_challenge.return_value = None  # Simulate a successful async call

    payload = {
        "channel_id": "test-channel",
        "return_url": "https://test.return.url",
        "settings": [
            {
                "label": "interval",
                "type": "text",
                "required": True,
                "default": "*/1 * * *",
            }
        ],
    }

    response = client.post(
        "/tick", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 202

    data = response.get_json()
    assert "message" in data
    assert data.get("message") == "Coding Challenge delivered"

    # Ensure the async function was called with the correct payload
    mock_coding_challenge.assert_called_once()


def test_tick_endpoint_invalid_payload(client):
    """Test the /tick endpoint with invalid payload (missing required fields)."""
    invalid_payload = {"channel_id": "test-channel"}  # Missing return_url and settings

    response = client.post(
        "/tick", data=json.dumps(invalid_payload), content_type="application/json"
    )
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data  # Error message should be returned
