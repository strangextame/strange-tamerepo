import unittest
from app import SearchService

class TestSearchService(unittest.TestCase):
    """Unit tests for the SearchService class."""

    def setUp(self):
        """Set up a new SearchService instance for each test."""
        self.search_service = SearchService()

    def test_validate_input_no_input(self):
        """Test validation fails when both card_name and card_type are empty."""
        error = self.search_service.validate_search_input(card_name="", card_type="")
        self.assertEqual(error, "Please enter a card name or select a card type to search.")

    def test_validate_input_name_too_long(self):
        """Test validation fails when card_name is too long."""
        long_name = "a" * 101
        error = self.search_service.validate_search_input(card_name=long_name, card_type="")
        self.assertEqual(error, "Card name is too long.")

    def test_validate_input_invalid_character(self):
        """Test validation fails when card_name contains an invalid character."""
        error = self.search_service.validate_search_input(card_name="Sol Ring #", card_type="")
        self.assertEqual(error, "Card name contains an invalid character: '#'")

    def test_validate_input_invalid_char_in_exact_search(self):
        """Test validation fails for invalid characters within exact search syntax."""
        error = self.search_service.validate_search_input(card_name='!"Sol Ring$!"', card_type="")
        self.assertEqual(error, "Card name contains an invalid character: '$'")

    def test_validate_input_valid_name_only(self):
        """Test validation passes with a valid card name."""
        error = self.search_service.validate_search_input(card_name="Lightning Bolt", card_type="")
        self.assertIsNone(error)

    def test_validate_input_valid_type_only(self):
        """Test validation passes with a valid card type."""
        error = self.search_service.validate_search_input(card_name="", card_type="Creature")
        self.assertIsNone(error)

    def test_validate_input_valid_name_and_type(self):
        """Test validation passes with both a valid name and type."""
        error = self.search_service.validate_search_input(card_name="Birds of Paradise", card_type="Creature")
        self.assertIsNone(error)

    def test_validate_input_valid_exact_search(self):
        """Test validation passes for a valid name using exact search syntax."""
        error = self.search_service.validate_search_input(card_name='!"Counterspell"', card_type="")
        self.assertIsNone(error)

    def test_validate_input_valid_complex_name(self):
        """Test validation passes for a name with various allowed characters."""
        error = self.search_service.validate_search_input(card_name="Jace, the Mind Sculptor", card_type="")
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()