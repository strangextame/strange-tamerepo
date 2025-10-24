"""
Pytest-based tests for the Flask application routes and basic functionality.
"""

import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # You can add test-specific configuration here if needed
    # For example: app.config.update({"TESTING": True, ...})
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"MTG Card Finder" in response.data
    assert b"Search for a Magic: The Gathering card" in response.data

def test_search_for_known_card(client):
    """Test searching for a specific, well-known card."""
    response = client.post('/search', data={'search_query': 'Sol Ring', 'card_type': ''})
    assert response.status_code == 200
    assert b"Results for \"Sol Ring\"" in response.data
    assert b"Sol Ring" in response.data # Check that the card name is in the results
    assert b"Add {C}{C}" in response.data # Check for part of the card text

def test_autocomplete(client):
    """Test the autocomplete endpoint."""
    response = client.get('/autocomplete?q=sol')
    assert response.status_code == 200
    suggestions = response.get_json()
    assert isinstance(suggestions, list)
    assert "Sol Ring" in suggestions