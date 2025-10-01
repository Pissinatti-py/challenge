import random
from typing import Optional, List
from dataclasses import dataclass

from src.models.player import Player, PlayerBehavior
from src.models.board import Board
from src.services.logging import logger


@dataclass
class GameResult:
    """
    Stores the results of a single game simulation.
    """

    winner: Player
    total_turns: int
    game_duration: int
    final_standings: List[tuple[str, int, int]]
    timeout: bool = False


class AutoRunner:
    """
    Automatic game runner that simulates property trading games.
    Handles game flow, turn management, and win conditions.
    """

    MAX_TURNS = 1000  # Maximum turns to prevent infinite games
    INITIAL_BALANCE = 300
    LAP_BONUS = 100

    def __init__(self, initial_balance: int = INITIAL_BALANCE):
        """
        Initializes the game runner with players and board.

        :param initial_balance: Starting balance for each player
        :type initial_balance: int
        """
        self.initial_balance = initial_balance
        self.players = self._create_players()
        self.board = Board(players=self.players)
        self.current_turn = 0
        self.game_active = False

    def _create_players(self) -> List[Player]:
        """
        Creates the four players with different behaviors.

        :return: List of players
        :rtype: List[Player]
        """
        return [
            Player("Impulsivo", PlayerBehavior.IMPULSIVE, self.initial_balance),
            Player("Exigente", PlayerBehavior.DEMANDING, self.initial_balance),
            Player("Cauteloso", PlayerBehavior.CAUTIOUS, self.initial_balance),
            Player("Aleatório", PlayerBehavior.RANDOM, self.initial_balance),
        ]

    def _roll_dice(self) -> int:
        """
        Simulates rolling a six-sided dice.

        :return: Random number between 1 and 6
        :rtype: int
        """
        return random.randint(1, 6)

    def _get_active_players(self) -> List[Player]:
        """
        Returns list of players still in the game.

        :return: List of active players
        :rtype: List[Player]
        """
        return [player for player in self.players if player.is_active]

    def _execute_player_turn(self, player: Player) -> bool:
        """
        Executes a single turn for a player.

        :param player: The player taking their turn
        :type player: Player
        :return: True if turn completed successfully, False if player went bankrupt
        :rtype: bool
        """
        # Roll dice and move
        dice_value = self._roll_dice()
        logger.info(f"{player.name} Rolled {dice_value} on dice.")

        new_position = player.move(dice_value, len(self.board.properties))
        current_property = self.board.get_property(new_position)

        logger.info(
            f"Player position {player.name}, {new_position}, {current_property.name}"
        )

        # Handle property interaction
        if current_property.is_owned():
            # Pay rent if owned by another player
            if current_property.owner != player:
                success = player.pay_rent(current_property)
                if not success:
                    return False  # Player went bankrupt
        else:
            # Try to buy if available
            player.buy_property(current_property)

        return True

    def _check_win_condition(self) -> Optional[Player]:
        """
        Checks if there's a winner (only one active player remaining).

        :return: The winning player or None if game continues
        :rtype: Optional[Player]
        """
        active_players = self._get_active_players()

        if len(active_players) == 1:
            return active_players[0]

        return None

    def _display_game_status(self):
        """
        Displays current status of all players.
        """
        logger.info("\n" + "=" * 60)
        logger.info("📊 GAME STATUS")
        logger.info("=" * 60)

        for player in self.players:
            if player.is_active:
                assets = player.get_total_assets()
                logger.info(
                    f"✅ {player.name}: ${player.balance} | "
                    f"Propriedades: {len(player.properties_owned)} | "
                    f"Total: ${assets}"
                )
            else:
                logger.info(f"❌ {player.name}: FALIDO")

        logger.info("=" * 60 + "\n")

    def _get_final_standings(self) -> List[tuple[str, int, int]]:
        """
        Gets final standings sorted by total assets.

        :return: List of (name, balance, properties_count) tuples
        :rtype: List[tuple[str, int, int]]
        """
        standings = []
        for player in self.players:
            standings.append(
                (player.name, player.balance, len(player.properties_owned))
            )

        # Sort by balance (descending)
        standings.sort(key=lambda x: x[1], reverse=True)
        return standings

    def run(self, show_status_every: int = 100) -> GameResult:
        """
        Runs a complete game simulation from start to finish.

        :param show_status_every: Show status every N turns (0 to disable)
        :type show_status_every: int
        :return: Game results including winner and statistics
        :rtype: GameResult
        """
        players_count = len(self.players)
        logger.info(f"Game stating with {players_count} players.")
        self.game_active = True
        self.current_turn = 0
        timeout = False

        # Game loop
        while self.game_active and self.current_turn < self.MAX_TURNS:
            self.current_turn += 1

            # Show periodic status updates
            if show_status_every > 0 and self.current_turn % show_status_every == 0:
                logger.info(f"\n🕐 Turno {self.current_turn}")
                self._display_game_status()

            # Each active player takes a turn
            for player in self.players:
                if not player.is_active:
                    continue

                logger.info(f"{player.name} Turn #{self.current_turn}")

                # Execute turn
                self._execute_player_turn(player)

                # Check for winner after each turn
                winner = self._check_win_condition()
                if winner:
                    self.game_active = False
                    break

            # Check for timeout
            if self.current_turn >= self.MAX_TURNS:
                timeout = True
                logger.warning(f"⏰ Jogo atingiu limite de {self.MAX_TURNS} turnos!")

                # Winner is player with most assets
                active = self._get_active_players()
                winner = max(active, key=lambda p: p.get_total_assets())

        # Game ended - display results
        self._display_game_status()

        final_standings = self._get_final_standings()

        logger.info(f"The gamer winner was : {winner.name}")
        logger.info("\n" + "=" * 60)
        logger.info("🏆 CLASSIFICAÇÃO FINAL")
        logger.info("=" * 60)

        for i, (name, balance, props) in enumerate(final_standings, 1):
            logger.info(f"{i}º - {name}: ${balance} ({props} propriedades)")
        logger.info("=" * 60)

        return GameResult(
            winner=winner,
            total_turns=self.current_turn,
            game_duration=self.current_turn,
            final_standings=final_standings,
            timeout=timeout,
        )

    def reset(self):
        """
        Resets the game to initial state for a new simulation.
        """
        self.players = self._create_players()
        self.board = Board(players=self.players)
        self.current_turn = 0
        self.game_active = False
