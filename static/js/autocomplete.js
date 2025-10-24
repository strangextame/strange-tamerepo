document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURATION ---
    const searchInput = document.getElementById('card_name');
    const suggestionsPanel = document.getElementById('suggestions-panel');
    const autocompleteUrl = document.body.dataset.autocompleteUrl; // Get URL from data attribute
    let debounceTimer; // For debouncing API calls

    // Check if the elements were found
    if (!searchInput || !suggestionsPanel) {
        return;
    }
    if (!autocompleteUrl) {
        return;
    }

    // --- EVENT LISTENER ---
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer); // Clear any previous debounce timer

        debounceTimer = setTimeout(() => { // Start a new debounce timer
            const query = searchInput.value; // Get the LATEST value from the input
            if (query.length < 2) {
                suggestionsPanel.innerHTML = '';
                suggestionsPanel.style.display = 'none'; // Explicitly hide the panel
                return;
            }

            // Set the width of the suggestions panel to match the input field
            suggestionsPanel.style.width = searchInput.offsetWidth + 'px';

            fetch(`${autocompleteUrl}?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Network response was not ok (Status: ${response.status})`);
                    }
                    return response.json();
                })
                .then(data => {
                    suggestionsPanel.innerHTML = ''; // Clear previous suggestions
                    if (Array.isArray(data) && data.length > 0) {
                        data.forEach(item => {
                            const suggestionLink = document.createElement('a');
                            suggestionLink.href = '#';
                            suggestionLink.textContent = item;
                            suggestionLink.classList.add('list-group-item', 'list-group-item-action');
                            suggestionLink.addEventListener('click', function(e) {
                                e.preventDefault();
                                searchInput.value = item;
                                suggestionsPanel.style.display = 'none'; // Hide panel after selection
                            });
                            suggestionsPanel.appendChild(suggestionLink);
                        });
                        suggestionsPanel.style.display = 'block'; // Explicitly show the panel
                    } else {
                        suggestionsPanel.style.display = 'none'; // Hide if no suggestions
                    }
                })
                .catch(error => {
                    suggestionsPanel.style.display = 'none'; // Hide panel on any error
                });
        }, 250); // Debounce time: wait 250ms after the last keypress
    });

    // Add a listener to the whole document to hide suggestions when clicking away
    document.addEventListener('click', function(e) {
        // Hide the panel if the click is outside the search input and outside the panel itself
        if (e.target !== searchInput && !suggestionsPanel.contains(e.target)) {
            suggestionsPanel.style.display = 'none';
        }
    });
});