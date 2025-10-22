"""
MTG Card Finder Flask Application.

Provides a simple web interface to search Magic: The Gathering cards via the
Scryfall API.
"""

# We need 'request' to access the data sent by the user's form
from flask import Flask, jsonify, render_template, request, Response
# Import the Scryfall client wrapper
from markupsafe import Markup
from scryfall_client import fetch_autocomplete_suggestions, fetch_card
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

# Route to handle card search (POST only)
@app.route('/search', methods=['POST'])
def search() -> Response:
    """Handle card search requests.

    Retrieves the card name from the submitted form, queries the Scryfall API,
    and renders either the results page or an error page.

    Returns:
        flask.Response: Rendered ``results.html`` with card data or ``error.html`` with an error message.
    """
    # Get the card name that the user entered in the form
    card_name = request.form['card_name']
    card_type = request.form.get('card_type', '') # Use .get for the optional type
    # Sanitize and validate input
    card_name = card_name.strip()
    if not card_name:
        error_message = "Card name cannot be empty."
        return render_template('error.html', message=error_message)
    if len(card_name) > 100:
        error_message = "Card name is too long."
        return render_template('error.html', message=error_message)
    # Allow a wider range of characters including letters, numbers, spaces,
    # and common punctuation like apostrophes, commas, colons, and hyphens.
    if not re.fullmatch(r"[\w\s',:-]+", card_name):
        error_message = "Card name contains invalid characters."
        return render_template('error.html', message=error_message)

    # Build the Scryfall query string
    query = card_name
    if card_type:
        # Add the type filter to the query, e.g., "Sol Ring type:artifact"
        query += f" type:{card_type}"

    # Use the Scryfall client to fetch card data with timeout handling
    card_data = fetch_card(query)

    # Verify that we received data from the client
    if card_data:
        # card_data is already a dict from fetch_card
        
        # Extract the specific details we want to display
        # We use .get() as a safeguard in case a key is missing
        name = card_data.get('name')
        mana_cost = card_data.get('mana_cost', 'N/A')
        type_line = card_data.get('type_line')
        oracle_text = card_data.get('oracle_text')
        # image_uris may be missing; get nested 'normal' URL safely
        image_url = card_data.get('image_uris', {}).get('normal')
        
        # For multi-faced cards, the EDHREC link is on the first face.
        # Otherwise, it's on the top-level object.
        edhrec_link = card_data.get('related_uris', {}).get('edhrec')

    else:
        # Render a user‑friendly error page
        error_message = f"Sorry, no cards matching your search for '{card_name}' were found."
        return render_template('error.html', message=error_message)
    # Pass all this data to a new HTML template
    return render_template('results.html',
                           name=name,
                           mana_cost=mana_cost,
                           type_line=type_line,
                           oracle_text=oracle_text,
                           image_url=image_url,
                           edhrec_link=edhrec_link)

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