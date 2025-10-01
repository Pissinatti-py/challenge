from src.models.player import Player, PlayerBehavior
from src.models.property import Property

from tests.fixtures.game_fixtures import (
    impulsive_player,
    demanding_player,
    cautious_player,
    random_player,
    sample_property,
)


class TestPlayerInitialization:
    """Test suite for Player initialization"""

    def test_player_initialization(self):
        """Test that a player is correctly initialized"""
        player = Player("Test Player", PlayerBehavior.IMPULSIVE, 300)

        assert player.name == "Test Player"
        assert player.behavior == PlayerBehavior.IMPULSIVE
        assert player.balance == 300
        assert player.position == 0
        assert player.is_active
        assert len(player.properties_owned) == 0

    def test_player_default_balance(self):
        """Test that default balance is 300"""
        player = Player("Test", PlayerBehavior.IMPULSIVE)
        assert player.balance == 300


class TestPlayerBehaviors:
    """Test suite for different player behaviors"""

    def test_impulsive_always_buys(self, impulsive_player, sample_property):
        """Test that impulsive player always wants to buy"""
        assert impulsive_player.should_buy(sample_property)

    def test_demanding_buys_high_rent_only(self, demanding_player):
        """Test that demanding player only buys properties with rent > 50"""
        low_rent_property = Property(0, "Low Rent", 100, 40)
        high_rent_property = Property(1, "High Rent", 150, 60)

        assert not demanding_player.should_buy(low_rent_property)
        assert demanding_player.should_buy(high_rent_property)

    def test_cautious_keeps_reserve(self, cautious_player):
        """Test that cautious player maintains 80 balance reserve"""
        cheap_property = Property(0, "Cheap", 100, 10)
        expensive_property = Property(1, "Expensive", 250, 25)

        # With 300 balance: 300 - 100 = 200 >= 80 (should buy)
        assert cautious_player.should_buy(cheap_property)

        # With 300 balance: 300 - 250 = 50 < 80 (should not buy)
        assert not cautious_player.should_buy(expensive_property)

    def test_random_behavior_returns_boolean(self, random_player, sample_property):
        """Test that random player returns a boolean decision"""
        result = random_player.should_buy(sample_property)
        assert isinstance(result, bool)


class TestPlayerActions:
    """Test suite for player actions"""

    def test_player_can_buy_with_sufficient_funds(
        self, impulsive_player, sample_property
    ):
        """Test player can buy property when they have enough money"""
        assert impulsive_player.can_buy(sample_property)

    def test_player_cannot_buy_with_insufficient_funds(self, impulsive_player):
        """Test player cannot buy when they lack funds"""
        expensive_property = Property(0, "Expensive", 500, 50)
        assert not impulsive_player.can_buy(expensive_property)

    def test_buy_property_success(self, impulsive_player, sample_property):
        """Test successful property purchase"""
        initial_balance = impulsive_player.balance
        result = impulsive_player.buy_property(sample_property)

        assert result is True
        assert sample_property.owner == impulsive_player
        assert impulsive_player.balance == initial_balance - sample_property.sale_cost
        assert sample_property in impulsive_player.properties_owned

    def test_cannot_buy_owned_property(self, impulsive_player, sample_property):
        """Test that player cannot buy already owned property"""
        other_player = Player("Other", PlayerBehavior.IMPULSIVE)
        sample_property.buy(other_player)

        result = impulsive_player.buy_property(sample_property)
        assert result is False

    def test_pay_rent(self, impulsive_player, sample_property):
        """Test paying rent to property owner"""
        owner = Player("Owner", PlayerBehavior.IMPULSIVE, 300)
        sample_property.buy(owner)

        initial_balance = impulsive_player.balance
        owner_initial = owner.balance

        result = impulsive_player.pay_rent(sample_property)

        assert result is True
        assert impulsive_player.balance == initial_balance - sample_property.rent_value
        assert owner.balance == owner_initial + sample_property.rent_value

    def test_bankruptcy_on_negative_balance(self, impulsive_player):
        """Test that player goes bankrupt when balance becomes negative"""
        impulsive_player.balance = 5
        expensive_property = Property(0, "Expensive", 200, 100)
        owner = Player("Owner", PlayerBehavior.IMPULSIVE)
        expensive_property.buy(owner)

        result = impulsive_player.pay_rent(expensive_property)

        assert result is False
        assert not impulsive_player.is_active
        assert impulsive_player.balance < 0

    def test_bankruptcy_releases_properties(self, impulsive_player, sample_property):
        """Test that bankrupt player releases all properties"""
        impulsive_player.buy_property(sample_property)
        assert len(impulsive_player.properties_owned) == 1

        impulsive_player.go_bankrupt()

        assert not impulsive_player.is_active
        assert len(impulsive_player.properties_owned) == 0
        assert sample_property.owner is None


class TestPlayerMovement:
    """Test suite for player movement"""

    def test_player_moves_forward(self, impulsive_player):
        """Test that player moves forward on board"""
        new_position = impulsive_player.move(5, board_size=20)
        assert new_position == 5
        assert impulsive_player.position == 5

    def test_player_wraps_around_board(self, impulsive_player):
        """Test that player wraps around when reaching end of board"""
        impulsive_player.position = 18
        initial_balance = impulsive_player.balance

        new_position = impulsive_player.move(5, board_size=20)

        assert new_position == 3  # (18 + 5) % 20 = 3
        assert impulsive_player.balance == initial_balance + 100  # Lap bonus

    def test_receive_payment(self, impulsive_player):
        """Test that player can receive payments"""
        initial_balance = impulsive_player.balance
        impulsive_player.receive_payment(50)
        assert impulsive_player.balance == initial_balance + 50


class TestPlayerAssets:
    """Test suite for player asset calculations"""

    def test_total_assets_calculation(self, impulsive_player):
        """Test calculation of total assets"""
        prop1 = Property(0, "Prop1", 100, 10)
        prop2 = Property(1, "Prop2", 150, 15)

        impulsive_player.buy_property(prop1)
        impulsive_player.buy_property(prop2)

        # Initial: 300, spent: 250, balance: 50, properties: 250
        expected_assets = impulsive_player.balance + 250
        assert impulsive_player.get_total_assets() == expected_assets
