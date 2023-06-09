from flaskr import create_app
from flaskr.user import User
from flask_login import FlaskLoginClient
import unittest
from unittest.mock import patch
from unittest import mock
from unittest.mock import MagicMock
import pytest
from flaskr.user import User
import io
from io import BytesIO
# from flask.ext.testing import TestCase
"""Tests for pages."""


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app


@pytest.fixture
def client(app):
    app.test_client_class = FlaskLoginClient
    return app.test_client()


def test_nav(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<div id="nav_main_div">' in resp.data


"""This tests the page loading of the navigation bar template.
Run this test by running `pytest -v` in the /project directory.
"""


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<div id="home_main_div" class="main_div">' in resp.data


"""This tests the page loading of the homepage template.
Run this test by running `pytest -v` in the /project directory.
"""


def test_aliases(client):
    slash = client.get("/").data
    home = client.get("/home").data
    index = client.get("/index").data
    assert slash == home == index


"""This tests the page aliases for the homepage (/, /home, /index).
Run this test by running `pytest -v` in the /project directory.
"""

# TO - DO ----------------------------------------------------
# def test_pages(client):
#     resp = client.get("/pages")
#     assert resp.status_code == 200
#     assert b'<div id="pages_main_div" class="main_div">' in resp.data
"""This tests the page loading of the wiki pages overview template.
Run this test by running `pytest -v` in the /project directory.
"""

# TO - DO ----------------------------------------------------
# def test_about(client):
#     resp = client.get("/about")
#     assert resp.status_code == 200
#     assert b'<div id="about_main_div" class="main_div">' in resp.data
"""This tests the page loading of the about page template.
Run this test by running `pytest -v` in the /project directory.
"""

# TO - DO ----------------------------------------------------
# def test_page(client):
#     resp = client.get("/pages/0")
#     assert resp.status_code == 200
#     assert b'<div id="page_main_div" class="main_div">' in resp.data
"""This tests the page loading of each individual recipe page's template.
Run this test by running `pytest -v` in the /project directory.
"""


@pytest.fixture
def user_example():
    user = User('testing', "default")
    return user


def test_correct_signup(app, user_example):
    """Tests signup route when user attempts to create an
        account that did not previously exist. Used MagicMock to
        prevent from creating a new account everytime we test.
    """
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_up'):
        with app.test_client() as client:
            data = {"Username": 'testing', "Password": 'somepassword'}
            response = client.post('/check_signup', data=data)
            response = client.get('/')

            assert response.status_code == 200
            assert "Hi testing!" in response.text


def test_wrong_signup(app, user_example):
    """Tests signup route when user attempts to create an
        account with the wrong parameters.
    """
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_up'):
        with app.test_client() as client:
            data = {"Username": None, "Password": 'password'}
            response = client.post('/check_signup', data=data)

            print("RESPONSE HERE:" + response.text)

            assert response.status_code == 400
            assert "Bad Request" in response.text


def test_correct_login(app, user_example):
    """Tests login route when user attempts to login with an
        account that already exists and the password is correct.
    """
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_in'):
        with app.test_client() as client:
            data = {"Username": "Nicole", "Password": 'somepassword'}
            response = client.post('/check_login', data=data)
            response = client.get('/')

            assert response.status_code == 200
            assert "Hi Nicole!" in response.text


def test_wrong_login(app, user_example):
    """Tests login route when user attempts to login with an
        account that already exists but the parameters are wrong.
    """
    app.test_client_class = FlaskLoginClient
    with patch('flaskr.backend.Backend.sign_in'):
        with app.test_client() as client:
            data = {"Username": None, "Password": 'password'}
            response = client.post('/check_login', data=data)

            print("RESPONSE HERE:" + response.text)

            assert response.status_code == 400
            assert "Bad Request" in response.text


def test_logout(app, user_example):
    """Tests logout route when user attempts to logout from 
       their account.
    """
    app.test_client_class = FlaskLoginClient
    with app.test_client() as client:
        response = client.post('/logout')
        response = client.get('/')

        assert response.status_code == 200
        assert not "Hi testin!" in response.text


def test_upload_no_file(app):
    app.test_client_class = FlaskLoginClient

    user = User("testing@gmail.com", "default")

    with patch('flaskr.backend.Backend.upload'):

        with app.test_client(user=user) as client:

            data = {'file': (BytesIO(b"abcdef"), '')}

            response = client.post('/upload', data=data)
            print(response.text)
            assert "No selected file" in response.text


""" Tests that upload file returns correct message when no file is given

By patching in the client and also patching a user, as the user needs to be logged in in order to upload something,
we can test that our upload function is returning the correct message when no file is given, which should be "No selected file"

We do this by creating fake "data" in order to be able to pass it into our upload. Once we call upload with client.post,
we can check if our expected message is inside our response using response.text, which checks HTML. 

Args:
    Since we are patching everything inside the test, we are only passing in our "app" as to create the testing environment

Returns:
    Returns True or False depending on if the assertion was succesfull or not
"""


def test_upload_invalid_file(app):
    app.test_client_class = FlaskLoginClient

    user = User("testing@gmail.com", "default")

    with patch('flaskr.backend.Backend.upload'):

        with app.test_client(user=user) as client:

            data = {'file': (BytesIO(b"abcdef"), 'test.mp4')}

            response = client.post('/upload', data=data)
            print(response.text)
            assert "Not a valid file format" in response.text


""" Tests that upload file returns correct message when file is incorrect format

By patching in the client and also patching a user, as the user needs to be logged in in order to upload something,
we can test that our upload function is returning the correct message when the file is not a correct format, which should be "Not a valid file format"

We do this by creating fake "data" in order to be able to pass it into our upload. Once we call upload with client.post,
we can check if our expected message is inside our response using response.text, which checks HTML. 

Args:
    Since we are patching everything inside the test, we are only passing in our "app" as to create the testing environment

Returns:
    Returns True or False depending on if the assertion was succesfull or not
"""


def test_upload_successful(app):
    app.test_client_class = FlaskLoginClient

    user = User("testing@gmail.com", "default")

    with patch('flaskr.backend.Backend.upload'):

        with app.test_client(user=user) as client:

            data = {'file': (BytesIO(b"abcdef"), 'test.json')}

            response = client.post('/upload', data=data)
            print(response.text)
            assert "Succesfully uploaded" in response.text


""" Tests that upload file returns correct message when the file meets requirements

By patching in the client and also patching a user, as the user needs to be logged in in order to upload something,
we can test that our upload function is returning the correct message when the file meets all the requirements, which is "Succesfully uploaded"

We do this by creating fake "data" in order to be able to pass it into our upload. Once we call upload with client.post,
we can check if our expected message is inside our response using response.text, which checks HTML. 

Args:
    Since we are patching everything inside the test, we are only passing in our "app" as to create the testing environment

Returns:
    Returns True or False depending on if the assertion was succesfull or not
"""
# TO - DO
# def test_suggest_edits_valid_user(app):
#     app.test_client_class = FlaskLoginClient

#     user = User("testing@gmail.com")

#     with patch('flaskr.backend.Backend.upload'):

#         with app.test_client(user=user) as client:

#             data = 'suggest'

#             response = client.post("/pages/6", data=data)
#             print(response.data)
#             assert "<h2>Editing Mode</h2>" in response.text
""" Tests that edit mode is available if a user is logged in
We patch in a user with app.test_client() and then make a client.post in order to test

Args:
    Takes in an instance of app
Returns:
    Returns an assert statement finding if a certain block of text was found
"""

# TO - DO
# def test_suggest_edits_invalid_user(app):
#     app.test_client_class = FlaskLoginClient

#     with patch('flaskr.backend.Backend.upload'):

#         with app.test_client() as client:

#             data = 'Suggest Edits'

#             response = client.post("/pages/6", data=data)
#             print(response.data)
#             assert "<p>Please log in before submitting edits</p>" in response.text
""" Tests that if a user is not logged it will not let them edit any recipes
We don't create a user and then create a post method to obtain text.

Args:
    Takes in an instance of app
Returns:
    Returns an assert statement finding if a certain block of text was found
"""
