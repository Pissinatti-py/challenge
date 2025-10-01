from src.models.player import Player, PlayerBehavior

from tests.fixtures.game_fixtures import game_board


class TestBoardInitialization:
    """Test suite for Board initialization"""

    def test_board_creates_20_properties(self, game_board):
        """Test that board creates exactly 20 properties"""
        assert len(game_board.properties) == 20

    def test_all_properties_have_unique_positions(self, game_board):
        """Test that all properties have unique sequential positions"""
        positions = [prop.position for prop in game_board.properties]
        assert positions == list(range(20))

    def test_all_properties_have_names(self, game_board):
        """Test that all properties have names"""
        for prop in game_board.properties:
            assert prop.name is not None
            assert len(prop.name) > 0

    def test_all_properties_have_valid_costs(self, game_board):
        """Test that all properties have valid costs"""
        for prop in game_board.properties:
            assert prop.sale_cost > 0
            assert prop.rent_value > 0


class TestBoardOperations:
    """Test suite for Board operations"""

    def test_get_property_by_position(self, game_board):
        """Test retrieving property by position"""
        prop = game_board.get_property(5)
        assert prop is not None
        assert prop.position == 5

    def test_get_property_invalid_position(self, game_board):
        """Test getting property with invalid position returns None"""
        assert game_board.get_property(-1) is None
        assert game_board.get_property(25) is None

    def test_get_available_properties(self, game_board):
        """Test getting list of available properties"""
        available = game_board.get_available_properties()
        assert len(available) == 20  # All initially available

    def test_get_available_properties_after_purchase(self, game_board):
        """Test available properties decreases after purchase"""
        player = Player("Test", PlayerBehavior.IMPULSIVE)
        game_board.properties[0].buy(player)

        available = game_board.get_available_properties()
        assert len(available) == 19

    def test_get_owned_properties(self, game_board):
        """Test getting properties owned by specific player"""
        player = Player("Test", PlayerBehavior.IMPULSIVE)
        game_board.properties[0].buy(player)
        game_board.properties[5].buy(player)

        owned = game_board.get_owned_properties(player)
        assert len(owned) == 2
        assert all(prop.owner == player for prop in owned)
