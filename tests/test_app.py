import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, This is Krishna Jarhad!' in response.data