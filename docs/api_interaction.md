# Scryfall API Interaction

The application queries the **Scryfall** card database using the **named fuzzy search** endpoint:

```python
api_url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
response = requests.get(api_url)
```

## Request Details
- **Endpoint**: `https://api.scryfall.com/cards/named`
- **Query Parameter**: `fuzzy` – the card name entered by the user.  
  The fuzzy search tolerates misspellings and partial names, returning the closest matching card.

## Response Handling
- A successful request returns HTTP status **200** and a JSON payload containing card data.
- The code checks `response.status_code == 200` before processing.
- The JSON payload is parsed with `response.json()` and the following fields are extracted using `.get()` to guard against missing keys:
  - `name`
  - `mana_cost` (defaults to `'N/A'` if absent)
  - `type_line`
  - `oracle_text`
  - `image_uris['normal']` – nested lookup guarded with `.get('image_uris', {})`.

## Error Handling
- If the status code is not 200 (e.g., card not found), the user is shown an error page with a friendly message.
- The error message is constructed as:
  ```python
  error_message = f"Sorry, the card '{card_name}' was not found."
  ```

## Rate Limiting & Best Practices
- Scryfall imposes generous rate limits for typical use. For production or high‑traffic scenarios, consider adding caching or exponential back‑off.
- Always validate or sanitize user input if extending the API usage beyond the provided fuzzy search.
