import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from flaskr.backend import Backend
from flask.testing import FlaskClient
import io
from io import BytesIO

"""Tests for Backend."""

def test_upload():

    test_blob = MagicMock()
    test_bucket = MagicMock()
    test_storage_client = MagicMock()

    test_storage_client.bucket.return_value = test_bucket
    test_bucket.blob.return_value = test_blob

    with patch('google.cloud.storage.Client', return_value = test_storage_client):
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

#I believe this is technically not a unit test bc the pages are not static
def test_get_all_pages_content():
    data = Backend.get_all_pages(None)
    assert data[0]["name"] == "Bunny Dango"
    assert data[1]["name"] == "Butterscotch Cinnamon Pie"

def test_get_wiki_page():
    page_data = Backend.get_wiki_page(None, 2)
    assert page_data["id"] == '2'
    assert page_data["name"] == "Rare Candy"
    
def test_get_wiki_page_wrong():
    page_data = Backend.get_wiki_page(None, 2)
    assert page_data["id"] == '2'
    assert page_data["name"] != "Not so Rare Candy"

def test_get_wiki_page_none():
    page_data = Backend.get_wiki_page(None, -1)
    try:
        assert page_data["id"] == "This cannot be accessed"
    except TypeError:
        pass
