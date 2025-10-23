"""
MTG Card Finder Flask Application.

Provides a simple web interface to search Magic: The Gathering cards via the
Scryfall API.
"""

# We need 'request' to access the data sent by the user's form
from flask import Flask, jsonify, render_template, request, Response
# Import the Scryfall client wrapper
from markupsafe import Markup # Markup is used for the mana filter
from scryfall_client import fetch_autocomplete_suggestions, fetch_cards # Changed from fetch_card to fetch_cards
import re

app = Flask(__name__)

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

def _validate_card_name(card_name: str) -> str | None:
    """
    Validates the card name against a set of rules.
    Returns an error message string if validation fails, otherwise None.
    """
    if not card_name:
        return "Card name cannot be empty."
    if len(card_name) > 100:
        return "Card name is too long."
    if not re.fullmatch(r"[\w\s',:/-]+", card_name):
        return "Card name contains invalid characters."
    return None

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
    card_name = card_name.strip()
    error_message = _validate_card_name(card_name)
    if error_message:
        return render_template('error.html', message=error_message)

    # Build the Scryfall query string
    query = card_name
    if card_type:
        # Add the type filter to the query, e.g., "Sol Ring type:artifact"
        query += f" type:{card_type}"

    # Use the Scryfall client to fetch a page of cards
    search_result = fetch_cards(query, page=page)

    # Verify that we received data from the client
    if search_result and search_result.get("data"):
        # Pass the list of cards and all necessary pagination data to the template
        return render_template('results.html',
                               cards=search_result.get("data", []),
                               search_term=card_name,
                               card_type=card_type,
                               page=page,
                               has_more=search_result.get("has_more", False),
                               total_cards=search_result.get("total_cards", 0)
                               )
    else:
        # Render a user‑friendly error page
        error_message = f"Sorry, no cards matching your search for '{query}' were found."
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
    app.run(debug=True)