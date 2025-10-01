from abc import ABC, abstractmethod
from enum import Enum
import random
from typing import Optional

from src.services.logging import logger


class PlayerBehavior(Enum):
    """
    Enum representing the different player behavior types in the game.
    Each behavior defines a unique strategy for property purchasing decisions.
    """

    IMPULSIVE = "Impulsivo"
    DEMANDING = "Exigente"
    CAUTIOUS = "Cauteloso"
    RANDOM = "Aleatório"


class BehaviorStrategy(ABC):
    """
    Abstract base class for player behavior strategies.
    Implements the Strategy pattern for different purchasing behaviors.
    """

    @abstractmethod
    def should_buy(self, player: "Player", property) -> bool:
        """
        Determines whether the player should purchase a property based on their strategy.

        :param player: The player making the decision
        :type player: Player
        :param property: The property being considered for purchase
        :type property: Property
        :return: True if the player should buy, False otherwise
        :rtype: bool
        """
        pass


class ImpulsiveBehavior(BehaviorStrategy):
    """
    Impulsive behavior strategy.
    This player buys any property they land on, without any conditions.
    """

    def should_buy(self, player: "Player", property) -> bool:
        """
        Always returns True - impulsive players buy everything.

        :param player: The player making the decision
        :type player: Player
        :param property: The property being considered
        :type property: Property
        :return: Always True
        :rtype: bool
        """
        return True


class DemandingBehavior(BehaviorStrategy):
    """
    Demanding behavior strategy.
    This player only buys properties with rent value greater than 50.
    """

    def should_buy(self, player: "Player", property) -> bool:
        """
        Returns True only if the property rent value exceeds 50.

        :param player: The player making the decision
        :type player: Player
        :param property: The property being considered
        :type property: Property
        :return: True if rent value > 50, False otherwise
        :rtype: bool
        """
        return property.rent_value > 50


class CautiousBehavior(BehaviorStrategy):
    """
    Cautious behavior strategy.
    This player only buys if they will have at least 80 balance remaining after purchase.
    """

    def should_buy(self, player: "Player", property) -> bool:
        """
        Returns True only if the player will have at least 80 balance after buying.

        :param player: The player making the decision
        :type player: Player
        :param property: The property being considered
        :type property: Property
        :return: True if remaining balance >= 80, False otherwise
        :rtype: bool
        """
        return (player.balance - property.sale_cost) >= 80


class RandomBehavior(BehaviorStrategy):
    """
    Random behavior strategy.
    This player buys properties with a 50% probability.
    """

    def should_buy(self, player: "Player", property) -> bool:
        """
        Returns True or False with equal 50% probability.

        :param player: The player making the decision
        :type player: Player
        :param property: The property being considered
        :type property: Property
        :return: Random True or False
        :rtype: bool
        """
        return random.choice([True, False])


class Player:
    """
    Represents a player in the property trading game.
    Each player has a behavior strategy, balance, position, and collection of properties.
    """

    BEHAVIOR_MAP = {
        PlayerBehavior.IMPULSIVE: ImpulsiveBehavior(),
        PlayerBehavior.DEMANDING: DemandingBehavior(),
        PlayerBehavior.CAUTIOUS: CautiousBehavior(),
        PlayerBehavior.RANDOM: RandomBehavior(),
    }

    def __init__(self, name: str, behavior: PlayerBehavior, initial_balance: int = 300):
        """
        Initializes a new player with specified behavior and starting balance.

        :param name: The player's name
        :type name: str
        :param behavior: The player's behavior type
        :type behavior: PlayerBehavior
        :param initial_balance: Starting money amount, defaults to 300
        :type initial_balance: int, optional
        """
        self.name = name
        self.behavior = behavior
        self.strategy = self.BEHAVIOR_MAP[behavior]
        self.balance = initial_balance
        self.position = 0
        self.is_active = True
        self.properties_owned = []

    def can_buy(self, property) -> bool:
        """
        Checks if the player has enough money to purchase a property.

        :param property: The property to check
        :type property: Property
        :return: True if player has sufficient funds, False otherwise
        :rtype: bool
        """
        return self.balance >= property.sale_cost

    def should_buy(self, property) -> bool:
        """
        Determines if the player wants to buy the property based on their behavior strategy.

        :param property: The property being considered
        :type property: Property
        :return: True if the player should buy, False otherwise
        :rtype: bool
        """
        if not self.can_buy(property):
            return False

        return self.strategy.should_buy(self, property)

    def buy_property(self, property) -> bool:
        """
        Attempts to purchase a property if it's available and the player wants to buy it.
        Deducts the cost from balance and adds property to owned list.

        :param property: The property to purchase
        :type property: Property
        :return: True if purchase was successful, False otherwise
        :rtype: bool
        """
        if not property.is_owned() and self.should_buy(property):
            old_balance = self.balance
            self.balance -= property.sale_cost
            property.buy(self)
            self.properties_owned.append(property)

            logger.debug(f"{self.name}, {property.name}, {property.sale_cost}")
            logger.warning(f"{self.name}, {old_balance}, {self.balance}")

            return True

        return False

    def pay_rent(self, property) -> bool:
        """
        Pays rent to the property owner when landing on their property.
        Player goes bankrupt if balance becomes negative.

        :param property: The property the player landed on
        :type property: Property
        :return: True if payment was successful, False if player went bankrupt
        :rtype: bool
        """
        if property.owner and property.owner != self:
            old_balance = self.balance
            self.balance -= property.rent_value
            property.owner.receive_payment(property.rent_value)

            logger.debug(
                f"{self.name}, {property.owner.name}, {property.name}, {property.rent_value}"
            )
            logger.warning(f"{self.name}, {old_balance}, {self.balance}")

            if self.balance < 0:
                self.go_bankrupt()
                return False

        return True

    def receive_payment(self, amount: int):
        """
        Adds money to the player's balance (from rent payments or bonuses).

        :param amount: The amount of money to receive
        :type amount: int
        """
        old_balance = self.balance
        self.balance += amount
        logger.info(f"{self.name}, {old_balance}, {self.balance}")

    def go_bankrupt(self):
        """
        Marks the player as bankrupt and releases all their properties.
        The player is no longer active in the game.
        """
        self.is_active = False
        logger.error(self.name)

        # Release all properties back to the market
        for property in self.properties_owned:
            property.owner = None

        self.properties_owned.clear()

    def move(self, steps: int, board_size: int = 20):
        """
        Moves the player forward on the board by the specified number of steps.
        Awards bonus money if the player completes a full lap around the board.

        :param steps: Number of positions to move forward
        :type steps: int
        :param board_size: Total number of positions on the board, defaults to 20
        :type board_size: int, optional
        :return: The player's new position on the board
        :rtype: int
        """
        old_position = self.position
        self.position = (self.position + steps) % board_size

        # Check if player completed a full lap
        if self.position < old_position:
            self.receive_payment(100)  # Bonus for completing a lap
            logger.info(f"🔄 {self.name} completou uma volta e recebeu $100!")

        return self.position

    def get_total_assets(self) -> int:
        """
        Calculates the player's total wealth (balance + property values).

        :return: Total assets value
        :rtype: int
        """
        properties_value = sum(prop.sale_cost for prop in self.properties_owned)
        return self.balance + properties_value

    def __str__(self):
        """
        Returns a human-readable string representation of the player.

        :return: Formatted player information
        :rtype: str
        """
        status = "Ativo" if self.is_active else "Falido"
        return (
            f"{self.name} ({self.behavior.value}) - "
            f"Saldo: ${self.balance} - "
            f"Propriedades: {len(self.properties_owned)} - "
            f"Status: {status}"
        )

    def __repr__(self):
        """
        Returns a technical string representation of the player object.

        :return: Player object representation
        :rtype: str
        """
        return f"Player(name='{self.name}', behavior={self.behavior}, balance={self.balance})"
