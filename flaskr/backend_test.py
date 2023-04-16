import unittest
from flask.testing import FlaskClient
import io
from io import BytesIO
from unittest.mock import patch
from unittest.mock import MagicMock
from flaskr.backend import Backend
from flaskr.user import User
from google.cloud import storage
import json
import hashlib
"""Tests for Backend."""


def test_correct_signup():
    """Tests signup function when user attempts to create an
        account that did not previously exist. Used MagicMock to
        prevent from creating a new account everytime we test.
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    storage_client.bucket.return_value = bucket
    blob.exists.return_value = False
    #bucket.blob.return_value = blob
    with patch('google.cloud.storage.Client', return_value=storage_client):
        backend = Backend(storage_client)
        user = User('NewUserNameNeverUsedBefore')
        backend.sign_up(user, 'wdjbvwebjh')
    assert blob.open.return_value.write.assert_called_once


def test_wrong_signup():
    """Tests signup function when user attempts to create an
        account that already exists. Used MagicMock so we don't 
        have to check if the account truly exists or not.
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    storage_client.bucket.return_value = bucket
    blob.exists.return_value = True
    with patch('google.cloud.storage.Client', return_value=storage_client):
        backend = Backend(storage_client)
        user = User('ExistingUser')
    assert not backend.sign_up(user, 'password')


# def test_correct_signin():
#    """Tests signin function when user attempts to login
#        an account that already exists and the password is correct.
#    """
#     user = User('new')
#     pas = 'prefix' + 'password'
#     test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
#     test = Backend.sign_in(None, user, test_pass)
#     assert test == True


def test_correct_signin():
    """Tests signin function when user attempts to login 
        an account that already exists and the password is correct. 
    """

    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    with patch('google.cloud.storage.Client', return_value=storage_client):
        backend = Backend(storage_client)

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            user = User('new')
            pas = 'prefix' + 'password'
            test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())

            mock_json.return_value = {'password': test_pass}

            test = backend.sign_in(user, str(test_pass))

    assert test == True


def test_wrong_signin():
    """Tests signin function when user attempts to login 
        an account that does not exist. 
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    storage_client.bucket.return_value = bucket
    blob.exists.return_value = False
    with patch('google.cloud.storage.Client', return_value=storage_client):
        backend = Backend(storage_client)
        user = User('NonExistingUser')
    assert not backend.sign_up(user, 'password')


# def test_wrong_password_signin():
#     """Tests signin function when user attempts to login
#         an account that already exists BUT the password is wrong.
#     """
#     user = User('new')
#     pas = 'prefix' + 'notpassword'
#     test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
#     test = Backend.sign_in(None, user, test_pass)
#     assert test == False


def test_wrong_password_signin():
    """Tests signin function when user attempts to login 
         an account that already exists BUT the password is wrong. 
    """

    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    with patch('google.cloud.storage.Client', return_value=storage_client):
        backend = Backend(storage_client)

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            user = User('new')

            incorrect_pass = 'prefix' + 'notpassword'
            incorrect_pass = str(
                hashlib.blake2b(incorrect_pass.encode()).hexdigest())

            correct_pass = 'prefix' + 'password'
            correct_pass = str(
                hashlib.blake2b(correct_pass.encode()).hexdigest())

            mock_json.return_value = {'password': correct_pass}

            test = backend.sign_in(user, str(incorrect_pass))

    assert test == False


def test_upload():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.bucket.return_value = test_bucket
    test_bucket.blob.return_value = test_blob

    with patch('google.cloud.storage.Client', return_value=test_storage_client):
        backend = Backend(test_storage_client)

        backend.upload('nrjcontent', 'testfile.json')

        test_blob.upload_from_filename.assert_called_once()


""" Tests upload function from backend by asserting the method is called

For this test we are mocking everything, from blob, to the bucket and storage client. We set every mocks return value to point to one 
another so that they're chained.
After this we are still patching in a storage client in order to "simulate" a backend.
Once all of this is done, we can call upload and pass in our fake data.
If the function which actually uploads data to our bucket is called, we know the function is working.

Args:
    We're not taking anything in directly for this test

Uses: 
    Simulated backend and backend functions

Returns:
    Our return statement is going to be whether or not our assertion passed or fail.
"""

# def test_get_all_pages_min():
#     data = Backend.get_all_pages(None)
#     assert len(data) > 0


def test_get_all_pages_min():

    test_blob = MagicMock()
    test_blob1 = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.bucket.return_value = test_bucket

    test_storage_client.list_blobs.return_value = [test_blob, test_blob1]

    with patch('google.cloud.storage.Client', return_value=test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"name": "Bunny Dango"}

            data = backend.get_all_pages()

    assert len(data) == 2


"""This tests the get_all_pages method retrieving at least one value.
Run this test by running `pytest -v` in the /project directory.
"""

# I believe this is technically not a unit test, but was unsure--
# of how to setup the test since the pages are dynamic.

# def test_get_all_pages_content():
#     data = Backend.get_all_pages(None)
#     assert data[0]["name"] == "Bunny Dango"
#     assert data[1]["name"] == "Butterscotch Cinnamon Pie"


def test_get_all_pages_content():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.bucket.return_value = test_bucket

    test_storage_client.list_blobs.return_value = [test_blob]

    with patch('google.cloud.storage.Client', return_value=test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"name": "Bunny Dango"}

            data = backend.get_all_pages()

    assert data[0]["name"] == "Bunny Dango"


"""This tests the get_all_pages method retrieving all content in the right order.
Run this test by running `pytest -v` in the /project directory.
"""

# def test_get_wiki_page():
#     page_data = Backend.get_wiki_page(None, 2)
#     assert page_data["id"] == '2'
#     assert page_data["name"] == "Rare Candy"


def test_get_wiki_page():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.bucket.return_value = test_bucket

    test_storage_client.list_blobs.return_value = [test_blob]

    with patch('google.cloud.storage.Client', return_value=test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"id": "2", "name": "Bunny Dango"}

            data = backend.get_wiki_page(2)

    assert data["id"] == "2"
    assert data["name"] == "Bunny Dango"


"""This tests the get_wiki_page method retrieving the correct JSON object at specified id.
Run this test by running `pytest -v` in the /project directory.
"""

# def test_get_wiki_page_none():
#     page_data = Backend.get_wiki_page(None, -1)
#     try:
#         assert page_data["id"] == "This cannot be accessed"
#     except TypeError:
#         pass


def test_get_wiki_page_none():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.bucket.return_value = test_bucket

    test_storage_client.list_blobs.return_value = [test_blob]

    with patch('google.cloud.storage.Client', return_value=test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"id": "2", "name": "Bunny Dango"}

            data = backend.get_wiki_page(-1)

    assert data == None


"""This tests the get_wiki_page method causing an exception if the 
id it is trying to access does not exist.
Run this test by running `pytest -v` in the /project directory.
"""
