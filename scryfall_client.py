"""
Scryfall API client module.

Provides a thin wrapper around the Scryfall card lookup endpoint with
type hints, timeout handling, and basic logging.
"""

import logging
from typing import Any, Dict, List, Optional

import requests

# Configure a module‑level logger. The application can configure the
# logging level globally if desired.
logger = logging.getLogger(__name__)
# This will be configured by app.py based on the active Flask configuration
SCRYFALL_API_BASE_URL = "https://api.scryfall.com"
session = requests.Session()

def fetch_cards(query: str, page: int = 1, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Retrieve a list of cards from the Scryfall API.

    Args:
        query: The Scryfall search query string.
        page: The page number of the results to fetch.
        timeout: Number of seconds to wait for the HTTP request before aborting.

    Returns:
        A dictionary containing card data and pagination info, or ``None``.
    """
    # Use the /search endpoint which is more flexible. `q=` is the query parameter.
    api_url = f"{SCRYFALL_API_BASE_URL}/cards/search"
    try:
        # The `q` parameter can include Scryfall's powerful search syntax.
        # We'll ask for cards in English and sorted by price for relevance
        params = {"q": f"{query} lang:en", "order": "usd", "page": page}
        response = session.get(api_url, params=params, timeout=timeout)
        if response.status_code == 200:
            search_results = response.json()
            if search_results.get("data"):
                logger.info("Successfully fetched %d cards for query '%s'.", len(search_results["data"]), query)
                # Return the whole search result object which includes pagination info
                return search_results
            logger.warning("Scryfall search for '%s' returned no results.", query)
            return None
        else:
            logger.warning(
                "Scryfall search for '%s' returned status %s.",
                response.status_code,
                query,
            )
            return None
    except requests.RequestException as exc:
        logger.exception("Scryfall search request failed for query '%s'.", query)
        return None

def fetch_autocomplete_suggestions(query: str, timeout: int = 5) -> List[str]:
    """
    Retrieve card name autocomplete suggestions from the Scryfall API.

    Args:
        query: The partial card name to get suggestions for.
        timeout: Request timeout in seconds.

    Returns:
        A list of card name strings.
    """
    api_url = f"{SCRYFALL_API_BASE_URL}/cards/autocomplete"
    try:
        response = session.get(api_url, params={"q": query}, timeout=timeout)
        if response.status_code == 200:
            results = response.json()
            suggestions = results.get('data', [])
            logger.info("Fetched %d suggestions for query '%s'.", len(suggestions), query)
            return suggestions
        else:
            logger.warning("Scryfall autocomplete for '%s' returned status %s.", query, response.status_code)
            return []
    except requests.RequestException as exc:
        logger.exception("Scryfall autocomplete request failed for query '%s'.", query)
        return []