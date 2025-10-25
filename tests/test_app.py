"""
Unit tests for the Flask application endpoints using pytest.
"""

import pytest
import requests

from app import create_app

# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def app_instance():
    """Create and configure a new Flask app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app_instance):
    """A test client for the Flask app."""
    return app_instance.test_client()


# -----------------------------
# Tests
# -----------------------------

def test_main_page(client):
    """Test that the main page returns 200 and contains HTML content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html>" in response.data


def test_ping(client):
    """Test the /ping endpoint returns 'pong'."""
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b"pong"


def test_health(client):
    """Test the /health endpoint returns correct JSON response."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'message' in data


def test_status(client):
    """Test the /status endpoint returns expected status info."""
    response = client.get('/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'Flask Application'
    assert data['status'] == 'running'


def test_info(client):
    """Test the /info endpoint returns app information."""
    response = client.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Sample Flask App'
    assert 'version' in data


def test_telaviv_earthquakes(client, monkeypatch):
    """Test /telaviv-earthquakes endpoint using a mocked USGS API response."""

    class MockResponse:
        """Mocked response object for requests.get."""
        status_code = 200

        def json(self):
            return {"features": []}

    # Patch requests.get to return the mock response
    monkeypatch.setattr(requests, "get", lambda url, params=None, timeout=None: MockResponse())

    response = client.get('/telaviv-earthquakes')
    assert response.status_code == 200
    data = response.get_json()
    assert 'events' in data
    assert data['count'] == 0


def test_graph_earthquakes_page(client):
    """Test the /graph-earthquakes page endpoint renders HTML correctly."""
    response = client.get('/graph-earthquakes')
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html>" in response.data
