# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `config.py` for managing environment-specific application settings (e.g., `DEBUG` mode).
- `requirements.txt` and `requirements-dev.txt` to separate production and development dependencies.
- `.flake8` configuration file to enforce consistent code style.
- Gunicorn as a production-ready WSGI server, added to `requirements.txt`.
- `CHANGELOG.md` to document project changes, following "Keep a Changelog" standards.
- `SearchService` class in `app.py` to encapsulate search-related business logic.
- Unit tests for `SearchService` in `test_services.py` to ensure validation logic is correct.
- A streamlined, icon-only theme toggle button in the footer for a cleaner UI.

### Changed
- **Refactored** `app.py` to load its configuration from `config.py`, removing hardcoded settings.
- **Refactored** `app.py` to delegate input validation to the `SearchService`, improving code structure and adhering to OOP principles.
- **Refactored** the theme-switching mechanism to use Bootstrap 5.3+'s native `data-bs-theme` system for better compatibility and persistence.
- **Updated** `README.md` with improved installation and running instructions, including sections for development and production environments.
- **Updated** `scryfall_client.py` to allow its `SCRYFALL_API_BASE_URL` to be configured dynamically from `app.py` based on the active environment.

### Deprecated

### Removed
- Removed the old custom theme-switching script (`static/js/theme.js`) and class-based logic (`<body class="dark">`).

### Fixed
- Resolved a `TypeError` on the search results page that occurred when an exact search returned no results.
- Corrected a logic error in `results.html` where cards would not display for non-ambiguous or type-only searches.
- Ensured the selected light/dark theme preference now correctly persists across all pages, including search results.

### Security

---

## [1.0.0] - 2024-05-20

### Added
- First release of the MTG Card Finder application.
- Core search functionality for Magic: The Gathering cards by name and/or type.
- "Smart" search feature that provides both an exact match and a broad search for ambiguous queries.
- Autocomplete for card names.
- Jinja2 filter (`mana`) to dynamically render mana symbols as images in search results.
- Pagination for search results.
- Basic Flask application structure with error handling for 404 and 500 status codes.