"""
MTG Card Finder Flask Application.

Provides a simple web interface to search Magic: The Gathering cards via the
Scryfall API.
"""

# We need 'request' to access the data sent by the user's form
from flask import Flask, render_template, request, Response
# Import the Scryfall client wrapper
from scryfall_client import fetch_card
import re

app = Flask(__name__)

@app.route('/')
def home() -> Response:
    """Render the home page with a search form.

    Returns:
        flask.Response: Rendered ``index.html`` template.
    """
    # This still just shows our main page with the search bar
    return render_template('index.html')

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
    # Sanitize and validate input
    card_name = card_name.strip()
    if not card_name:
        error_message = "Card name cannot be empty."
        return render_template('error.html', message=error_message)
    if len(card_name) > 100:
        error_message = "Card name is too long."
        return render_template('error.html', message=error_message)
    if not re.fullmatch(r"[A-Za-z0-9\-\s]+", card_name):
        error_message = "Card name contains invalid characters."
        return render_template('error.html', message=error_message)

    # Use the Scryfall client to fetch card data with timeout handling
    card_data = fetch_card(card_name)

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

        # Pass all this data to a new HTML template
        return render_template('results.html', 
                               name=name, 
                               mana_cost=mana_cost, 
                               type_line=type_line, 
                               oracle_text=oracle_text,
                               image_url=image_url)
    else:
        # Render a user‑friendly error page
        error_message = f"Sorry, the card '{card_name}' was not found."
        return render_template('error.html', message=error_message)

# Graceful error handlers
@app.errorhandler(404)
def not_found(error):
    """Render a user‑friendly 404 page."""
    return render_template('error.html', message="Page not found."), 404

@app.errorhandler(500)
def internal_error(error):
    """Render a user‑friendly 500 page."""
    return render_template('error.html', message="An unexpected error occurred."), 500

if __name__ == '__main__':
    app.run(debug=True)