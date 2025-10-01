from src.models.property import Property

from tests.fixtures.game_fixtures import sample_property, impulsive_player


class TestProperty:
    """Test suite for Property class"""

    def test_property_initialization(self):
        """Test that a property is correctly initialized"""
        prop = Property(0, "Test Property", 100, 10)

        assert prop.position == 0
        assert prop.name == "Test Property"
        assert prop.sale_cost == 100
        assert prop.rent_value == 10
        assert prop.owner is None

    def test_property_is_not_owned_initially(self, sample_property):
        """Test that a new property has no owner"""
        assert not sample_property.is_owned()

    def test_property_can_be_bought(self, sample_property, impulsive_player):
        """Test that a property can be assigned an owner"""
        sample_property.buy(impulsive_player)

        assert sample_property.is_owned()
        assert sample_property.owner == impulsive_player

    def test_property_string_representation_without_owner(self, sample_property):
        """Test string representation of unowned property"""
        result = str(sample_property)

        assert "Test Property" in result
        assert "Custo: $100" in result
        assert "Aluguel: $10" in result
        assert "Disponível" in result

    def test_property_string_representation_with_owner(
        self, sample_property, impulsive_player
    ):
        """Test string representation of owned property"""
        sample_property.buy(impulsive_player)
        result = str(sample_property)

        assert "Test Property" in result
        assert impulsive_player.name in result