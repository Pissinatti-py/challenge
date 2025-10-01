class Property:
    """
    The Property class represents a property on the game board.
    """

    def __init__(self, position: int, name: str, sale_cost: int, rent_value: int):
        self.position = position
        self.name = name
        self.sale_cost = sale_cost
        self.rent_value = rent_value
        self.owner = None

    def is_owned(self) -> bool:
        """
        Check if the property is owned by a player

        :return: True if owned, False otherwise
        :rtype: bool
        """
        return self.owner is not None

    def buy(self, player):
        """
        Assigns the property to a player

        :param player: The player buying the property
        :type player: Player
        """
        self.owner = player

    def __str__(self):
        owner_name = self.owner.name if self.owner else "Disponível"
        return f"{self.name} - Custo: ${self.sale_cost} - Aluguel: ${self.rent_value} - Dono: {owner_name}"
