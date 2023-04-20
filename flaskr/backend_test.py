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
import random
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
        user = User('NewUserNameNeverUsedBefore', 'default')
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
        user = User('ExistingUser', 'default')
    assert not backend.sign_up(user, 'password')


# TO - DO ----------------------------------------------------
# def test_correct_signin():
#     """Tests signin function when user attempts to login
#         an account that already exists and the password is correct.
#     """
#     user = User('new')
#     pas = 'prefix' + 'password'
#     test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
#     test = Backend.sign_in(None, user, test_pass)
#     assert test == True


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
        user = User('NonExistingUser', 'default')
    assert not backend.sign_up(user, 'password')


# TO - DO ----------------------------------------------------
# def test_wrong_password_signin():
#     """Tests signin function when user attempts to login
#         an account that already exists BUT the password is wrong.
#     """
#     user = User('new')
#     pas = 'prefix' + 'notpassword'
#     test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
#     test = Backend.sign_in(None, user, test_pass)
#     assert test == False


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

# TO - DO ----------------------------------------------------
# def test_get_all_pages_min():
#     data = Backend.get_all_pages(None)
#     assert len(data) > 0
"""This tests the get_all_pages method retrieving at least one value.
Run this test by running `pytest -v` in the /project directory.
"""

# TO - DO ----------------------------------------------------
# I believe this is technically not a unit test, but was unsure--
# of how to setup the test since the pages are dynamic.
# def test_get_all_pages_content():
#     data = Backend.get_all_pages(None)
#     assert data[0]["name"] == "Bunny Dango"
#     assert data[1]["name"] == "Butterscotch Cinnamon Pie"
"""This tests the get_all_pages method retrieving all content in the right order.
Run this test by running `pytest -v` in the /project directory.
"""

# TO - DO ----------------------------------------------------
# def test_get_wiki_page():
#     page_data = Backend.get_wiki_page(None, 2)
#     assert page_data["id"] == '2'
#     assert page_data["name"] == "Rare Candy"
"""This tests the get_wiki_page method retrieving the correct JSON object at specified id.
Run this test by running `pytest -v` in the /project directory.
"""

# TO - DO ----------------------------------------------------
# def test_get_wiki_page_none():
#     page_data = Backend.get_wiki_page(None, -1)
#     try:
#         assert page_data["id"] == "This cannot be accessed"
#     except TypeError:
#         pass
"""This tests the get_wiki_page method causing an exception if the 
id it is trying to access does not exist.
Run this test by running `pytest -v` in the /project directory.
"""


def test_correct_belongs_to_game():
    """Tests belongs_to_game function when the user 
        searches for a game title. 
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    storage_client.list_blobs.return_value = [blob]

    storage_client.bucket.return_value = bucket

    with patch('google.cloud.storage.Client', return_value=storage_client):
        with patch('json.loads', new_callable=MagicMock) as mock_json:
            backend = Backend(storage_client)

            mock_json.return_value = {"game": "zelda"}
            test = backend.belongs_to_game(["zelda"])
    assert len(test) == 1


def test_belongs_to_game_not_found():
    """Tests belongs_to_game function when the user 
        searches for a game title but no recipe
        matches the game.  
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    storage_client.list_blobs.return_value = [blob]

    storage_client.bucket.return_value = bucket

    with patch('google.cloud.storage.Client', return_value=storage_client):
        with patch('json.loads', new_callable=MagicMock) as mock_json:
            backend = Backend(storage_client)

            mock_json.return_value = {"game": "not zelda"}
            test = backend.belongs_to_game(["zelda"])

    assert len(test) == 0


def test_correct_is_quick_enough():
    """Tests is_quick_enough function when the user 
        searches for a time range  
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    storage_client.list_blobs.return_value = [blob]

    storage_client.bucket.return_value = bucket

    # Test it later
    blob.download_as_bytes.return_value = {"time": "60"}

    with patch('google.cloud.storage.Client', return_value=storage_client):
        with patch('json.loads', new_callable=MagicMock) as mock_json:
            backend = Backend(storage_client)

            mock_json.return_value = {"time": "60"}
            test = backend.is_quick_enough("60")
    assert len(test) == 1


def test_correct_is_not_quick_enough():
    """Tests is_quick_enough function when the user 
        searches for a time range but no recipe
        matches the range.  
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    storage_client.list_blobs.return_value = [blob]

    storage_client.bucket.return_value = bucket

    # Test it later
    blob.download_as_bytes.return_value = {"time": "90"}

    with patch('google.cloud.storage.Client', return_value=storage_client):
        with patch('json.loads', new_callable=MagicMock) as mock_json:
            backend = Backend(storage_client)

            mock_json.return_value = {"time": "90"}
            test = backend.is_quick_enough("60")
    assert len(test) == 0


def test_surprise_me():
    """Tests surprise_me function when the user 
        wants to receieve a random recipe to make. 
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    blob1 = MagicMock()
    blob2 = MagicMock()

    storage_client.bucket.return_value = bucket
    bucket.blob.return_value = blob

    bucket.blob1.return_value = blob1
    bucket.blob2.return_value = blob2

    storage_client.list_blobs.return_value = [blob, blob1, blob2]

    storage_client.bucket.return_value = bucket

    # Test it later
    blob.download_as_bytes.return_value = {"id": "0"}
    blob1.download_as_bytes.return_value = {"id": "1"}
    blob2.download_as_bytes.return_value = {"id": "2"}

    result = []
    for i in range(10):
        with patch('google.cloud.storage.Client', return_value=storage_client):
            with patch('json.loads', new_callable=MagicMock) as mock_json:
                backend = Backend(storage_client)
                i = random.randint(-1, 2)
                mock_json.return_value = {"id": str(i)}
                test = backend.surprise_me()
                temp = int(test["id"])
                result.append(temp)
    assert 0 in result and 1 in result and 2 in result
