from flaskr import create_app
from flaskr.user import User
from flask_login import FlaskLoginClient

import unittest
from unittest.mock import patch
from unittest import mock

import pytest

import io
from io import BytesIO

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
    app.test_client_class = FlaskLoginClient    
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
# def test_home_page(client):
#     resp = client.get("/")
#     assert resp.status_code == 200
#     assert b"Hello, World!\n" in resp.data

# TODO(Project 1): Write tests for other routes.


def test_upload_no_file(app):
    app.test_client_class = FlaskLoginClient

    user = User("testing@gmail.com")

    with patch('flaskr.backend.Backend.upload'):

        with app.test_client(user=user) as client:

            data = {'file': (BytesIO(b"abcdef"), '')}

            response = client.post('/upload',data = data)
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

    user = User("testing@gmail.com")

    with patch('flaskr.backend.Backend.upload'):

        with app.test_client(user=user) as client:

            data = {'file': (BytesIO(b"abcdef"), 'test.mp4')}

            response = client.post('/upload',data = data)
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

    user = User("testing@gmail.com")

    with patch('flaskr.backend.Backend.upload'):

        with app.test_client(user=user) as client:

            data = {'file': (BytesIO(b"abcdef"), 'test.jpg')}
          
            response = client.post('/upload',data = data)
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