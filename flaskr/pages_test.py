from flaskr import create_app

import pytest
from flaskr.user import User
from unittest.mock import MagicMock
from flask_login import FlaskLoginClient
from unittest.mock import patch

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

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    #assert b"Hello, World!\n" in resp.data

# TODO(Project 1): Write tests for other routes.

@pytest.fixture
def user_example():
    user = User('testing')
    return user

def test_correct_signup(app, user_example):
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_up'):
        with app.test_client() as client:
            data = {"Username" : 'testing' , "Password" : 'somepassword'}
            response = client.post('/check_signup', data = data) 
            response = client.get('/')
            print("RESPONSE HERE:" + response.text)

            assert response.status_code == 200
            assert "Hi testing!" in response.text

def test_wrong_signup(app, user_example):
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_up'):
        with app.test_client() as client:
            data = {"Username" : None , "Password" : 'password'}
            response = client.post('/check_signup', data = data) 

            print("RESPONSE HERE:" + response.text)

            assert response.status_code == 400
            assert "Bad Request" in response.text

def test_correct_login(app, user_example):
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_in'):
        with app.test_client() as client:
            data = {"Username" : "Nicole" , "Password" : 'somepassword'}
            response = client.post('/check_login', data = data) 
            response = client.get('/')

            assert response.status_code == 200
            assert "Hi Nicole!" in response.text

def test_wrong_login(app, user_example):
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_in'):
        with app.test_client() as client:
            data = {"Username" : None , "Password" : 'password'}
            response = client.post('/check_login', data = data) 

            print("RESPONSE HERE:" + response.text)

            assert response.status_code == 400
            assert "Bad Request" in response.text

def test_logout(app, user_example):
    app.test_client_class = FlaskLoginClient
    with app.test_client() as client:
            response = client.post('/logout') 
            response = client.get('/')

            assert response.status_code == 200
            assert not "Hi testin!" in response.text

