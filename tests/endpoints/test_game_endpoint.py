from tests.endpoints.client import client


class TestGameEndpoints:
    """Test suite for game API endpoints"""

    def test_simulate_single_game(self, client):
        """Test single game simulation endpoint"""
        response = client.get("api/v1/game/simulate")

        assert response.status_code == 200
        data = response.json()

        assert "winner" in data
        assert "total_turns" in data
        assert "timeout" in data
        assert "players" in data
        assert "final_standings" in data

        assert len(data["players"]) == 4
        assert len(data["final_standings"]) == 4

    def test_simulate_multiple_games_default(self, client):
        """Test multiple game simulations with default parameters"""
        response = client.get("api/v1/game/simulate/multiple")

        assert response.status_code == 200
        data = response.json()

        assert data["total_simulations"] == 2
        assert "wins_by_behavior" in data
        assert "win_percentages" in data
        assert "average_turns" in data
        assert "timeout_count" in data

    def test_simulate_multiple_games_custom_count(self, client):
        """Test multiple simulations with custom count"""
        response = client.get("api/v1/game/simulate/multiple?simulations=10")

        assert response.status_code == 200
        data = response.json()

        assert data["total_simulations"] == 10

    def test_simulate_multiple_games_validation(self, client):
        """Test validation for simulation count"""
        # Test minimum
        response = client.get("api/v1/game/simulate/multiple?simulations=0")
        assert response.status_code == 422

        # Test maximum
        response = client.get("api/v1/game/simulate/multiple?simulations=101")
        assert response.status_code == 422

    def test_api_documentation_available(self, client):
        """Test that API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
