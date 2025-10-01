import pytest
from src.models.player import Player, PlayerBehavior
from src.models.property import Property
from src.models.board import Board
from src.services.runner import AutoRunner


@pytest.fixture
def sample_property():
    """
    Creates a sample property for testing.

    :return: A property instance
    :rtype: Property
    """
    return Property(position=0, name="Test Property", sale_cost=100, rent_value=10)


@pytest.fixture
def impulsive_player():
    """
    Creates an impulsive player for testing.

    :return: An impulsive player instance
    :rtype: Player
    """
    return Player("Test Impulsive", PlayerBehavior.IMPULSIVE, initial_balance=300)


@pytest.fixture
def demanding_player():
    """
    Creates a demanding player for testing.

    :return: A demanding player instance
    :rtype: Player
    """
    return Player("Test Demanding", PlayerBehavior.DEMANDING, initial_balance=300)


@pytest.fixture
def cautious_player():
    """
    Creates a cautious player for testing.

    :return: A cautious player instance
    :rtype: Player
    """
    return Player("Test Cautious", PlayerBehavior.CAUTIOUS, initial_balance=300)


@pytest.fixture
def random_player():
    """
    Creates a random player for testing.

    :return: A random player instance
    :rtype: Player
    """
    return Player("Test Random", PlayerBehavior.RANDOM, initial_balance=300)


@pytest.fixture
def game_board():
    """
    Creates a game board for testing.

    :return: A board instance
    :rtype: Board
    """
    return Board()


@pytest.fixture
def auto_runner():
    """
    Creates an AutoRunner instance for testing.

    :return: An AutoRunner instance
    :rtype: AutoRunner
    """
    return AutoRunner()
