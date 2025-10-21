"""
Scryfall API client module.

Provides a thin wrapper around the Scryfall card lookup endpoint with
type hints, timeout handling, and basic logging.
"""

import logging
from typing import Any, Dict, Optional

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

def fetch_card(card_name: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Retrieve card data from the Scryfall API.

    Args:
        card_name: The name (or fuzzy name) of the card to look up.
        timeout: Number of seconds to wait for the HTTP request before aborting.

    Returns:
        A dictionary with the card data if the request succeeds and the card is
        found, otherwise ``None``.
    """
    api_url = f"{SCRYFALL_API_BASE_URL}/cards/named"
    try:
        response = session.get(api_url, params={"fuzzy": card_name}, timeout=timeout)
        if response.status_code == 200:
            logger.info("Successfully fetched card data for '%s'.", card_name)
            return response.json()
        else:
            logger.warning(
                "Scryfall returned status %s for card '%s'.",
                response.status_code,
                card_name,
            )
            return None
    except requests.RequestException as exc:
        logger.error("Error contacting Scryfall for card '%s': %s", card_name, exc)
        return None