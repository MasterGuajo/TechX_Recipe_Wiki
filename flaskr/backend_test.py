from flaskr.backend import Backend
from flaskr.user import User
from unittest.mock import MagicMock
from unittest.mock import patch
from google.cloud import storage
import json
import hashlib
# TODO(Project 1): Write tests for Backend methods.

def test_correct_signup():
    """Tests signup route/function when user attempts to create an
        account that did not previously exist. Used MagicMock to
        prevent from creating a new account everytime we test.
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    storage_client.bucket.return_value = bucket
    blob.exists.return_value = False
    #bucket.blob.return_value = blob
    with patch('google.cloud.storage.Client', return_value = storage_client):
        backend = Backend(storage_client)
        user = User('NewUserNameNeverUsedBefore')
        backend.sign_up(user, 'wdjbvwebjh')
    assert blob.open.return_value.write.assert_called_once

def test_wrong_signup():
    """Tests signup route/function when user attempts to create an
        account that already exists. Used MagicMock so we don't 
        have to check if the account truly exists or not.
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    storage_client.bucket.return_value = bucket
    blob.exists.return_value = True
    with patch('google.cloud.storage.Client', return_value = storage_client):
        backend = Backend(storage_client)
        user = User('ExistingUser')
    assert not backend.sign_up(user, 'password')

def test_correct_signin():
    """Tests signin route/function when user attempts to login 
        an account that already exists and the password is correct. 
    """
    user = User('new')
    pas = 'prefix'+'password'
    test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
    test = Backend.sign_in(None, user, test_pass)
    assert test == True

def test_wrong_signin():
    """Tests signin route/function when user attempts to login 
        an account that does not exist. 
    """
    storage_client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    storage_client.bucket.return_value = bucket
    blob.exists.return_value = False
    with patch('google.cloud.storage.Client', return_value = storage_client):
        backend = Backend(storage_client)
        user = User('NonExistingUser')
    assert not backend.sign_up(user, 'password')


def test_wrong_password_signin():
    """Tests signin route/function when user attempts to login 
        an account that already exists BUT the password is wrong. 
    """
    user = User('new')
    pas = 'prefix'+'notpassword'
    test_pass = str(hashlib.blake2b(pas.encode()).hexdigest())
    test = Backend.sign_in(None, user, test_pass)
    assert test == False

