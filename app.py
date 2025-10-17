# We need 'request' to access the data sent by the user's form
from flask import Flask, render_template, request
# We need 'requests' to talk to the Scryfall API
import requests

app = Flask(__name__)

@app.route('/')
def home():
    # This still just shows our main page with the search bar
    return render_template('index.html')

# This is a new route that will handle the card search
# methods=['POST'] means this route will only respond to POST requests (from a form)
@app.route('/search', methods=['POST'])
def search():
    # Get the card name that the user entered in the form
    card_name = request.form['card_name']

    # Build the API URL and make the request to Scryfall
    api_url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    response = requests.get(api_url)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        card_data = response.json()
        
        # Extract the specific details we want to display
        # We use .get() as a safeguard in case a key is missing
        name = card_data.get('name')
        mana_cost = card_data.get('mana_cost', 'N/A')
        type_line = card_data.get('type_line')
        oracle_text = card_data.get('oracle_text')
        image_url = card_data.get('image_uris', {}).get('normal')

        # Pass all this data to a new HTML template
        return render_template('results.html', 
                               name=name, 
                               mana_cost=mana_cost, 
                               type_line=type_line, 
                               oracle_text=oracle_text, 
                               image_url=image_url)
    else:
        # If the card isn't found, show an error page
        error_message = f"Sorry, the card '{card_name}' was not found."
        return render_template('error.html', message=error_message)

if __name__ == '__main__':
    app.run(debug=True)