import pytest
import requests
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_main_page(client):
    """Test that the main page returns 200 and HTML."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html>" in response.data

def test_ping(client):
    """Test the /ping endpoint."""
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b"pong"

def test_health(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'message' in data

def test_status(client):
    """Test the /status endpoint."""
    response = client.get('/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'Flask Application'
    assert data['status'] == 'running'

def test_info(client):
    """Test the /info endpoint."""
    response = client.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Sample Flask App'
    assert 'version' in data

def test_telaviv_earthquakes(client, monkeypatch):
    """Test /telaviv-earthquakes endpoint using mocked requests."""
    import json


    class MockResponse:
        status_code = 200
        def json(self):
            return {"features": []}

    monkeypatch.setattr(requests, "get", lambda url, params=None: MockResponse())
    response = client.get('/telaviv-earthquakes')
    assert response.status_code == 200
    data = response.get_json()
    assert 'events' in data
    assert data['count'] == 0

def test_graph_earthquakes_page(client):
    """Test graph page endpoint."""
    response = client.get('/graph-earthquakes')
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html>" in response.data
