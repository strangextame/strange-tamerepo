"""
MTG Card Finder Flask Application.

Provides a web interface to search Magic: The Gathering cards.
This module handles web routing and delegates search logic to the SearchService.
"""

# We need 'request' to access the data sent by the user's form
from flask import Flask, jsonify, render_template, request, Response
from config import get_config
# Import the Scryfall client wrapper
from markupsafe import Markup
# Import specific functions to use them directly
from scryfall_client import fetch_autocomplete_suggestions, fetch_cards
import scryfall_client # Import the module itself to access its variables
import re

class SearchService:
    """
    Encapsulates the business logic for validating and preparing card searches.
    """
    _ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ',:/-")

    def validate_search_input(self, card_name: str, card_type: str) -> str | None:
        """
        Validates the search inputs.
        Returns an error message string if validation fails, otherwise None.
        """
        if not card_name and not card_type:
            return "Please enter a card name or select a card type to search."

        if len(card_name) > 100:
            return "Card name is too long."

        name_to_check = card_name.strip('!"') if card_name.startswith('!"') and card_name.endswith('"') else card_name
        for char in name_to_check:
            if char not in self._ALLOWED_CHARS:
                return f"Card name contains an invalid character: '{char}'"

        return None

app = Flask(__name__)
app.config.from_object(get_config()) # Load configuration dynamically
scryfall_client.SCRYFALL_API_BASE_URL = app.config['SCRYFALL_API_BASE_URL'] # Configure Scryfall client
search_service = SearchService() # Create a single instance of our service

@app.template_filter('mana')
def mana_symbols(mana_cost_str: str) -> Markup:
    """
    A Jinja2 filter to convert mana symbols like {W} in a string into images.
    Example: "{T}: Add {C}{C}" -> "<img>: Add <img><img>"
    """
    if not mana_cost_str or mana_cost_str == 'N/A':
        return 'N/A'

    def replace_with_img(match):
        """This function is called for each matched mana symbol."""
        symbol = match.group(0)
        # Sanitize the symbol code for the URL (e.g., {2/U} -> 2U)
        symbol_code = symbol.strip('{}').replace('/', '').upper()
        return f'<img src="https://svgs.scryfall.io/card-symbols/{symbol_code}.svg" alt="{symbol}" class="mana-symbol" title="{symbol}">'

    # Use re.sub to find all mana symbols and replace them using our helper function
    # The result is wrapped in Markup to tell Jinja it's safe to render as HTML
    return Markup(re.sub(r'({[^}]+})', replace_with_img, mana_cost_str))

@app.route('/')
def home() -> Response:
    """Render the home page with a search form.

    Returns:
        flask.Response: Rendered ``index.html`` template.
    """
    # This still just shows our main page with the search bar
    return render_template('index.html')

# Route to provide autocomplete suggestions
@app.route('/autocomplete')
def autocomplete() -> Response:
    """Provide card name suggestions for the search bar."""
    # Get the partial query from the 'q' URL parameter
    query = request.args.get('q', '')

    # Don't bother searching for very short queries
    if len(query) < 2:
        return jsonify([])

    # Fetch suggestions from our Scryfall client
    suggestions = fetch_autocomplete_suggestions(query)

    # Return the list of suggestions as a JSON response
    return jsonify(suggestions)

# Route to handle card search (handles POST for new search, GET for pagination)
@app.route('/search', methods=['GET', 'POST'])
def search() -> Response:
    """Handle card search requests.

    Retrieves the card name from the submitted form, queries the Scryfall API,
    and renders either the results page or an error page.

    Returns:
        flask.Response: Rendered ``results.html`` with card data or ``error.html`` with an error message.
    """
    if request.method == 'POST':
        # New search from the form
        card_name = request.form.get('search_query', '')
        card_type = request.form.get('card_type', '')
        page = 1
    else: # request.method == 'GET'
        # Navigating via pagination links
        card_name = request.args.get('search_query', '')
        card_type = request.args.get('card_type', '')
        # Ensure page is an integer, default to 1
        page = request.args.get('page', 1, type=int)


    # --- Input validation and query building ---
    original_search_term = card_name.strip()
    error_message = search_service.validate_search_input(original_search_term, card_type)
    if error_message:
        return render_template('error.html', message=error_message)

    # --- Overhauled Search Logic ---
    # For new searches, we perform two queries:
    # 1. An "exact" search for the top autocomplete result (most likely card).
    # 2. A "broad" search for the user's original term.
    # This allows us to present both result sets in a tabbed interface.

    exact_search_term = None
    exact_results = None
    broad_results = None
    is_ambiguous_search = False

    # Only perform "smart" exact/broad search if a card name was provided
    if original_search_term:
        if request.method == 'POST':
            suggestions = fetch_autocomplete_suggestions(original_search_term)
            if suggestions:
                exact_search_term = suggestions[0]
                # Only perform two searches if the top suggestion is different from the user's term
                if original_search_term.lower() != exact_search_term.lower():
                    is_ambiguous_search = True
                    # 1. Get the exact results
                    exact_query = f'!"{exact_search_term}"'
                    if card_type: exact_query += f" type:{card_type}"
                    exact_results = fetch_cards(exact_query, page=1)

            # 2. Get the broad results (or the only results if search was already exact)
            broad_query = original_search_term
            if card_type: broad_query += f" type:{card_type}"
            broad_results = fetch_cards(broad_query, page=page)

        else: # GET request for pagination
            # For pagination, we only need to query for the broad results.
            broad_query = original_search_term
            if card_type: broad_query += f" type:{card_type}"
            broad_results = fetch_cards(broad_query, page=page)
    else: # No card name provided, so it's a type-only search
        query = f"type:{card_type}"
        broad_results = fetch_cards(query, page=page)

    # Determine which result set to use for the main display
    search_result = broad_results

    # Verify that we received data from the client
    if search_result and search_result.get("data"):
        # Pass the list of cards and all necessary pagination data to the template
        return render_template('results.html',
                               # "All Cards" is now the default, so it gets the main 'cards' variable
                               cards=search_result.get("data", []),
                               # Pass exact results separately for the secondary tab
                               exact_search_cards=exact_results.get("data") if is_ambiguous_search and exact_results else [],
                               search_term=original_search_term, # Display what the user typed
                               is_ambiguous_search=is_ambiguous_search,
                               exact_search_term=exact_search_term,
                               card_type=card_type,
                               page=page,
                               has_more=search_result.get("has_more", False),
                               total_cards=search_result.get("total_cards", 0)
                               )
    else:
        # Render a user‑friendly error page
        error_message = f"Sorry, no cards matching your search for '{original_search_term}' were found."
        return render_template('error.html', message=error_message)

# Graceful error handlers
@app.errorhandler(404)
def not_found(error):
    """Render a user-friendly 404 page."""
    return render_template('error.html', message="Page not found."), 404

@app.errorhandler(500)
def internal_error(error):
    """Render a user‑friendly 500 page."""
    return render_template('error.html', message="An unexpected error occurred."), 500

if __name__ == '__main__':
    # Use the debug setting from the configuration
    app.run(debug=app.config.get('DEBUG', False))