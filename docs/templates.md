# Template Documentation

This document describes each Jinja2 HTML template used by the MTG Card Finder application and the context variables it expects.

## `templates/index.html`

- **Purpose**: Home page that displays a search form for the user to enter a card name.
- **Context Variables**: None required.
- **Key Elements**:
  - `<form action="/search" method="post">` – submits the card name to the `/search` route.

## `templates/results.html`

- **Purpose**: Displays the details of a card returned from the Scryfall API.
- **Context Variables**:
  - `name` – Card name (string).
  - `mana_cost` – Mana cost string (or `'N/A'` if unavailable).
  - `type_line` – Card type line (string).
  - `oracle_text` – Rules text of the card (string).
  - `image_url` – Direct URL to the card image (string).
- **Key Elements**:
  - `{{ image_url }}` – shows the card image.
  - `{{ name }}`, `{{ mana_cost }}`, `{{ type_line }}`, `{{ oracle_text }}` – displayed in the details section.

## `templates/error.html`

- **Purpose**: Shows an error message when a card cannot be found or the API request fails.
- **Context Variables**:
  - `message` – Human‑readable error description (string).
- **Key Elements**:
  - `{{ message }}` – rendered inside a paragraph element.

All templates are located in the `templates/` directory and are rendered via Flask’s `render_template` function.