from flaskr import create_app

import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    resp = client.get("/")
    #html = resp.data.decode()
    assert resp.status_code == 200
    assert b"This is main.html" in resp.data
    assert b"A familiar beam of light shines down. The beam of light descends onto a stage. Lightning flashes to reveal Prince Charming riding his valiant steed Chauncey across the open plains. The wind blows back his golden mane." in resp.data

"""def test_pages_page(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data
    
def test_home_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data
# TODO(Project 1): Write tests for other routes."""
