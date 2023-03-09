from flaskr.backend import Backend

"""Tests for Backend."""

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
