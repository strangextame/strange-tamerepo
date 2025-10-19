import json
from app import app

with app.test_client() as client:
    # Test home page
    home_resp = client.get('/')
    print("Home status:", home_resp.status_code)

    # Test a known card (e.g., Lightning Bolt)
    search_resp = client.post('/search', data={'card_name': 'Lightning Bolt'})
    print("Search status:", search_resp.status_code)

    # Print a snippet of the response data (first 200 characters)
    snippet = search_resp.data.decode('utf-8')[:200]
    print("Search response snippet:", snippet)