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
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

SCRYFALL_API_BASE_URL = "https://api.scryfall.com"
session = requests.Session()

def fetch_card(query: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Retrieve card data from the Scryfall API.

    Args:
        query: The Scryfall search query string.
        timeout: Number of seconds to wait for the HTTP request before aborting.

    Returns:
        A dictionary with the card data if the request succeeds and the card is
        found, otherwise ``None``.
    """
    # Use the /search endpoint which is more flexible. `q=` is the query parameter.
    api_url = f"{SCRYFALL_API_BASE_URL}/cards/search"
    try:
        # The `q` parameter can include Scryfall's powerful search syntax.
        response = session.get(api_url, params={"q": query}, timeout=timeout)
        if response.status_code == 200:
            search_results = response.json()
            # The /search endpoint returns a list of cards in the 'data' key.
            # We'll return the first result if it exists.
            if search_results.get("data"):
                logger.info("Successfully fetched card data for query '%s'.", query)
                return search_results["data"][0]
            logger.warning("Scryfall search for '%s' returned no results.", query)
            return None
        else:
            logger.warning(
                "Scryfall returned status %s for card '%s'.",
                response.status_code,
                query,
            )
            return None
    except requests.RequestException as exc:
        logger.error("Error contacting Scryfall for query '%s': %s", query, exc)
        return None

def fetch_autocomplete_suggestions(query: str, timeout: int = 3) -> List[str]:
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
            logger.warning("Autocomplete for '%s' returned status %s.", query, response.status_code)
            return []
    except requests.RequestException as exc:
        logger.error("Error contacting Scryfall for autocomplete on '%s': %s", query, exc)
        return []