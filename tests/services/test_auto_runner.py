from src.services.runner import AutoRunner, GameResult
from src.models.player import PlayerBehavior
from tests.fixtures.game_fixtures import auto_runner


class TestAutoRunnerInitialization:
    """Test suite for AutoRunner initialization"""

    def test_runner_creates_four_players(self, auto_runner):
        """Test that runner creates exactly 4 players"""
        assert len(auto_runner.players) == 4

    def test_runner_creates_all_behavior_types(self, auto_runner):
        """Test that runner creates one player of each behavior"""
        behaviors = [player.behavior for player in auto_runner.players]
        expected_behaviors = [
            PlayerBehavior.IMPULSIVE,
            PlayerBehavior.DEMANDING,
            PlayerBehavior.CAUTIOUS,
            PlayerBehavior.RANDOM,
        ]
        assert set(behaviors) == set(expected_behaviors)

    def test_runner_initializes_board(self, auto_runner):
        """Test that runner initializes board with properties"""
        assert auto_runner.board is not None
        assert len(auto_runner.board.properties) == 20

    def test_custom_initial_balance(self):
        """Test runner with custom initial balance"""
        runner = AutoRunner(initial_balance=500)
        assert all(player.balance == 500 for player in runner.players)


class TestAutoRunnerGameFlow:
    """Test suite for game flow"""

    def test_roll_dice_returns_valid_value(self, auto_runner):
        """Test that dice roll returns value between 1 and 6"""
        for _ in range(100):
            roll = auto_runner._roll_dice()
            assert 1 <= roll <= 6

    def test_get_active_players(self, auto_runner):
        """Test getting list of active players"""
        active = auto_runner._get_active_players()
        assert len(active) == 4  # All active initially

        # Bankrupt one player
        auto_runner.players[0].go_bankrupt()
        active = auto_runner._get_active_players()
        assert len(active) == 3

    def test_check_win_condition_no_winner(self, auto_runner):
        """Test win condition when multiple players active"""
        winner = auto_runner._check_win_condition()
        assert winner is None

    def test_check_win_condition_with_winner(self, auto_runner):
        """Test win condition when only one player active"""
        # Bankrupt all but one player
        for player in auto_runner.players[1:]:
            player.go_bankrupt()

        winner = auto_runner._check_win_condition()
        assert winner == auto_runner.players[0]

    def test_execute_player_turn(self, auto_runner):
        """Test executing a single player turn"""
        player = auto_runner.players[0]
        initial_position = player.position

        result = auto_runner._execute_player_turn(player)

        assert result is True  # Turn completed successfully
        assert player.position != initial_position  # Player moved


class TestAutoRunnerSimulation:
    """Test suite for complete game simulation"""

    def test_run_completes_game(self, auto_runner):
        """Test that run method completes a game"""
        result = auto_runner.run(show_status_every=0)

        assert isinstance(result, GameResult)
        assert result.winner is not None
        assert result.total_turns > 0
        assert len(result.final_standings) == 4

    def test_game_respects_max_turns(self):
        """Test that game stops at max turns"""
        runner = AutoRunner()
        runner.MAX_TURNS = 10  # Set low limit for testing

        result = runner.run(show_status_every=0)

        assert result.total_turns <= 10
        if result.total_turns == 10:
            assert result.timeout is True

    def test_final_standings_format(self, auto_runner):
        """Test that final standings have correct format"""
        result = auto_runner.run(show_status_every=0)

        for standing in result.final_standings:
            name, balance, props = standing
            assert isinstance(name, str)
            assert isinstance(balance, int)
            assert isinstance(props, int)

    def test_reset_functionality(self, auto_runner):
        """Test that reset returns runner to initial state"""
        # Run a game
        auto_runner.run(show_status_every=0)

        # Reset
        auto_runner.reset()

        # Check reset state
        assert auto_runner.current_turn == 0
        assert auto_runner.game_active is False
        assert len(auto_runner.players) == 4
        assert all(player.is_active for player in auto_runner.players)
        assert all(player.balance == 300 for player in auto_runner.players)


class TestAutoRunnerStatistics:
    """Test suite for multiple simulations statistics"""

    def test_multiple_simulations(self):
        """Test running multiple simulations"""
        wins = {behavior.value: 0 for behavior in PlayerBehavior}
        num_simulations = 10

        for _ in range(num_simulations):
            runner = AutoRunner()
            result = runner.run(show_status_every=0)
            wins[result.winner.name] += 1

        # Check that wins are distributed (at least one behavior won)
        assert sum(wins.values()) == num_simulations
        assert any(count > 0 for count in wins.values())
