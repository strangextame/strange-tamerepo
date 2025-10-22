document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURATION ---
    const searchInput = document.getElementById('card_name');
    const suggestionsPanel = document.getElementById('suggestions-panel');
    const autocompleteUrl = document.body.dataset.autocompleteUrl; // Get URL from data attribute
    let debounceTimer; // For debouncing API calls

    // Check if the elements were found
    if (!searchInput || !suggestionsPanel) {
        console.error('CRITICAL ERROR: Could not find search input (ID: card_name) or suggestions panel (ID: suggestions-panel). Check your HTML IDs.');
        return;
    }
    if (!autocompleteUrl) {
        console.error('CRITICAL ERROR: Autocomplete URL is not set in the body data-autocomplete-url attribute. Check base.html.');
        return;
    }
    console.log('Autocomplete script loaded and initialized. (Mic Check #0)');

    // --- EVENT LISTENER ---
    searchInput.addEventListener('input', function() {
        console.log('Event: Input detected. (Mic Check #1)');
        clearTimeout(debounceTimer); // Clear any previous debounce timer

        debounceTimer = setTimeout(() => { // Start a new debounce timer
            const query = searchInput.value; // Get the LATEST value from the input
            if (query.length < 2) {
                console.log('Event: Query too short (< 2 chars). Clearing suggestions and hiding panel.');
                suggestionsPanel.innerHTML = '';
                suggestionsPanel.style.display = 'none'; // Explicitly hide the panel
                return;
            }
            console.log('Event: Query is long enough. Fetching for:', query, '(Mic Check #2)');

            // Set the width of the suggestions panel to match the input field
            suggestionsPanel.style.width = searchInput.offsetWidth + 'px';

            fetch(`${autocompleteUrl}?q=${encodeURIComponent(query)}`)
                .then(response => {
                    console.log('Fetch Step 1: Received network response (status:', response.status, response.statusText, '). (Mic Check #3)');
                    if (!response.ok) {
                        throw new Error(`Network response was not ok (Status: ${response.status})`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Fetch Step 2: Received data:', data, '(Mic Check #4)');
                    suggestionsPanel.innerHTML = ''; // Clear previous suggestions
                    if (Array.isArray(data) && data.length > 0) {
                        console.log('Populating panel with', data.length, 'suggestions.');
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
                        console.log('Received empty or non-array data. Hiding panel.');
                        suggestionsPanel.style.display = 'none'; // Hide if no suggestions
                    }
                })
                .catch(error => {
                    console.error('CRITICAL ERROR fetching autocomplete:', error);
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