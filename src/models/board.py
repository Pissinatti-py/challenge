from src.services.logging import logger
from src.models.property import Property


class Board:
    """
    The Board class represents the game board with its properties.
    """

    def __init__(self, players: list = None):
        self.properties = self._create_properties()
        self.players = players if players is not None else []
        self.current_turn = 0

    def _create_properties(self) -> list[Property]:
        """
        Makes a list of properties for the game board

        :return: The list of properties.
        :rtype: list[Property]
        """
        properties_data = [
            (0, "Avenida Atlântica", 100, 10),
            (1, "Rua Augusta", 80, 8),
            (2, "Avenida Paulista", 120, 12),
            (3, "Copacabana", 150, 15),
            (4, "Ipanema", 140, 14),
            (5, "Leblon", 160, 16),
            (6, "Jardins", 130, 13),
            (7, "Morumbi", 110, 11),
            (8, "Brooklin", 90, 9),
            (9, "Vila Madalena", 95, 9),
            (10, "Pinheiros", 105, 10),
            (11, "Itaim Bibi", 125, 12),
            (12, "Moema", 115, 11),
            (13, "Perdizes", 85, 8),
            (14, "Higienópolis", 135, 13),
            (15, "Barra da Tijuca", 145, 14),
            (16, "Botafogo", 75, 7),
            (17, "Flamengo", 70, 7),
            (18, "Tijuca", 65, 6),
            (19, "Centro", 60, 6),
        ]

        return [
            Property(pos, name, cost, rent) for pos, name, cost, rent in properties_data
        ]

    def get_property(self, position: int) -> Property:
        """
        Access a property by its position on the board

        :param position: The position of the property
        :type position: int
        :return: The property at the given position or None if out of range
        :rtype: Property
        """
        if 0 <= position < len(self.properties):
            return self.properties[position]

        return None

    def display_board(self):
        """
        Displays the current state of the game board
        """
        logger.info("\n=== Board ===")

        for prop in self.properties:
            logger.info(f"[{prop.position}] {prop}")

        logger.info("=" * 50)

    def get_available_properties(self) -> list[Property]:
        """
        The list of properties that are not owned by any player

        :return: The list of available properties
        :rtype: list[Property]
        """
        return [prop for prop in self.properties if not prop.is_owned()]

    def get_owned_properties(self, player) -> list[Property]:
        """
        The list of properties owned by a specific player

        :param player: The player whose properties to retrieve
        :type player: Player
        :return: The list of properties owned by the player
        :rtype: list[Property]
        """
        return [prop for prop in self.properties if prop.owner == player]
