"""
Unit tests for the Flask application endpoints using pytest.
"""
# pylint: disable=E0401

import pytest
import requests

from app import create_app# pylint: disable=E0401,C0413




# -----------------------------
# Fixtures
# -----------------------------

@pytest.fixture
def flask_app_instance_test():
    """Create and configure a new Flask app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(flask_app_instance):
    """A test client for the Flask app."""
    return flask_app_instance.test_client()


# -----------------------------
# Tests
# -----------------------------

def test_main_page(app_client):
    """Test that the main page returns 200 and contains HTML content."""
    response = app_client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html>" in response.data


def test_ping(client_application_flask):
    """Test the /ping endpoint returns 'pong'."""
    response = client_application_flask.get('/ping')
    assert response.status_code == 200
    assert response.data == b"pong"


def test_health(client_app):
    """Test the /health endpoint returns correct JSON response."""
    response = client_app.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'message' in data


def test_status(application_client):
    """Test the /status endpoint returns expected status info."""
    response = application_client.get('/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'Flask Application'
    assert data['status'] == 'running'


def test_info(client_application):
    """Test the /info endpoint returns app information."""
    response = client_application.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Sample Flask App'
    assert 'version' in data


def test_telaviv_earthquakes(application, monkeypatch):
    """Test /telaviv-earthquakes endpoint using a mocked USGS API response."""


    class MockResponse:# pylint: disable=too-few-public-methods
        """Mocked response object for requests.get."""
        status_code = 200

        def json(self):
            """json."""
            return {"features": []}

    # Patch requests.get to return the mock response
    monkeypatch.setattr(requests, "get", lambda url, params=None: MockResponse())

    response = application.get('/telaviv-earthquakes')
    assert response.status_code == 200
    data = response.get_json()
    assert 'events' in data
    assert data['count'] == 0


def test_graph_earthquakes_page(cl_app):
    """Test the /graph-earthquakes page endpoint renders HTML correctly."""
    response = cl_app.get('/graph-earthquakes')
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html>" in response.data
