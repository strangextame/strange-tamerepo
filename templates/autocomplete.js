document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURATION ---
    const searchInput = document.getElementById('card_name');
    const suggestionsPanel = document.getElementById('suggestions-panel');
    const autocompleteUrl = document.body.dataset.autocompleteUrl; // Get URL from data attribute

    // Check if the elements were found
    if (!searchInput || !suggestionsPanel) {
        console.error('Error: Could not find search input or suggestions panel. Check your HTML IDs.');
        return;
    }

    if (!autocompleteUrl) {
        console.error('Error: Autocomplete URL is not set in the body data-autocomplete-url attribute.');
        return;
    }

    // --- EVENT LISTENER ---
    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        // Only search if we have 2+ characters
        if (query.length > 1) {
            // Clear old suggestions
            suggestionsPanel.innerHTML = '';
            
            fetch(`${autocompleteUrl}?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Network response was not ok (Status: ${response.status})`);
                    }
                    return response.json(); // Try to parse the response as JSON
                })
                .then(data => {
                    if (Array.isArray(data) && data.length > 0) {
                        // Build the new dropdown
                        data.forEach(item => {
                            // Use <a> tags to make them look like Bootstrap items
                            const suggestionLink = document.createElement('a');
                            suggestionLink.href = '#'; // Make it a placeholder link
                            suggestionLink.textContent = item;
                            suggestionLink.classList.add('list-group-item', 'list-group-item-action');
                            
                            // Add click event to fill search box
                            suggestionLink.addEventListener('click', function(e) {
                                e.preventDefault(); // Stop link from navigating
                                searchInput.value = item;
                                suggestionsPanel.innerHTML = ''; // Hide panel
                            });
                            
                            suggestionsPanel.appendChild(suggestionLink);
                        });
                    }
                })
                .catch(error => {
                    console.error('CRITICAL ERROR fetching autocomplete:', error);
                });

        } else {
            // If text is too short, clear the panel
            suggestionsPanel.innerHTML = '';
        }
    });
});