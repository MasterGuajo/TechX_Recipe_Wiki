from flaskr import create_app
from unittest.mock import patch
import unittest
from flaskr.backend import Backend
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing

"""Tests for pages."""

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_nav(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<div id="nav_main_div">' in resp.data

def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<div id="home_main_div">' in resp.data

def test_aliases(client):
    slash = client.get("/").data
    home = client.get("/home").data
    index = client.get("/index").data
    assert slash == home == index

def test_pages(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b'<div id="pages_main_div">' in resp.data

def test_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b'<div id="about_main_div">' in resp.data

def test_page(client):
    resp = client.get("/pages/0")
    assert resp.status_code == 200
    assert b'<div id="page_main_div">' in resp.data
