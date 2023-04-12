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


def test_correct_signin():
    """Tests signin function when user attempts to login 
        an account that already exists and the password is correct. 
    """
    user = User('new')
    pas = 'prefix' + 'password'
    test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
    test = Backend.sign_in(None, user, test_pass)
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


def test_wrong_password_signin():
    """Tests signin function when user attempts to login 
        an account that already exists BUT the password is wrong. 
    """
    user = User('new')
    pas = 'prefix' + 'notpassword'
    test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
    test = Backend.sign_in(None, user, test_pass)
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


def test_get_all_pages_min():
    data = Backend.get_all_pages(None)
    assert len(data) > 0


"""This tests the get_all_pages method retrieving at least one value.
Run this test by running `pytest -v` in the /project directory.
"""


# I believe this is technically not a unit test, but was unsure--
# of how to setup the test since the pages are dynamic.
def test_get_all_pages_content():
    data = Backend.get_all_pages(None)
    assert data[0]["name"] == "Bunny Dango"
    assert data[1]["name"] == "Butterscotch Cinnamon Pie"


"""This tests the get_all_pages method retrieving all content in the right order.
Run this test by running `pytest -v` in the /project directory.
"""


def test_get_wiki_page():
    page_data = Backend.get_wiki_page(None, 2)
    assert page_data["id"] == '2'
    assert page_data["name"] == "Rare Candy"


"""This tests the get_wiki_page method retrieving the correct JSON object at specified id.
Run this test by running `pytest -v` in the /project directory.
"""


def test_get_wiki_page_none():
    page_data = Backend.get_wiki_page(None, -1)
    try:
        assert page_data["id"] == "This cannot be accessed"
    except TypeError:
        pass


"""This tests the get_wiki_page method causing an exception if the 
id it is trying to access does not exist.
Run this test by running `pytest -v` in the /project directory.
"""

def test_get_game_categories_one_category():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.list_blobs.return_value = [test_blob]

    test_storage_client.bucket.return_value = test_bucket

    with patch('google.cloud.storage.Client', return_value = test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"game": "Minecraft"}

            result = backend.get_game_categories()
        
    assert len(result) == 1
""" This test checks if there is one category in our json fields 
We mock a blob, bucket and storage client, while setting return values for out list_blobs and mock_json function
We also patch in our storage client and a json load
"""

def test_get_game_categories_no_category_field():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.list_blobs.return_value = [test_blob]

    test_storage_client.bucket.return_value = test_bucket

    with patch('google.cloud.storage.Client', return_value = test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"cate": "pie"}

            result = backend.get_game_categories()
        
    assert len(result) == 0
""" This test checks if there is no game field in our JSON 
We mock a blob, bucket and storage client, while setting return values for out list_blobs and mock_json function
We also patch in our storage client and a json load
"""

def test_get_game_categories_no_category_entry():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.list_blobs.return_value = [test_blob]

    test_storage_client.bucket.return_value = test_bucket

    with patch('google.cloud.storage.Client', return_value = test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"game": ""}

            result = backend.get_game_categories()
        
    assert len(result) == 0
""" This test checks if our game field is empty 
We mock a blob, bucket and storage client, while setting return values for out list_blobs and mock_json function
We also patch in our storage client and a json load
"""

def test_get_time_ranges_one_time_range():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.list_blobs.return_value = [test_blob]

    test_storage_client.bucket.return_value = test_bucket

    with patch('google.cloud.storage.Client', return_value = test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"time": "45"}

            result = backend.get_time_ranges()
        
    assert len(result) == 1
""" This test checks if there is one time range in our json fields 
We mock a blob, bucket and storage client, while setting return values for out list_blobs and mock_json function
We also patch in our storage client and a json load
"""

def test_get_time_range_no_time_field():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.list_blobs.return_value = [test_blob]

    test_storage_client.bucket.return_value = test_bucket

    with patch('google.cloud.storage.Client', return_value = test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"game": "Minecraft"}

            result = backend.get_time_ranges()
        
    assert len(result) == 0
""" This test checks if there is no time field in our JSON 
We mock a blob, bucket and storage client, while setting return values for out list_blobs and mock_json function
We also patch in our storage client and a json load
"""

def test_get_time_ranges_no_time_entry():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.list_blobs.return_value = [test_blob]

    test_storage_client.bucket.return_value = test_bucket

    with patch('google.cloud.storage.Client', return_value = test_storage_client):

        with patch('json.loads', new_callable=MagicMock) as mock_json:

            backend = Backend(test_storage_client)

            mock_json.return_value = {"time": ""}

            result = backend.get_time_ranges()
        
    assert len(result) == 0
""" This test checks if our time field is empty 
We mock a blob, bucket and storage client, while setting return values for out list_blobs and mock_json function
We also patch in our storage client and a json load
"""
