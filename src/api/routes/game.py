from fastapi import APIRouter, Query

from src.services.runner import AutoRunner
from src.schemas import (
    GameSimulationResponse,
    MultipleSimulationsResponse,
    PropertyResponse,
    PlayerResponse,
    FinalStanding,
)


router = APIRouter(prefix="/game", tags=["Game Simulation"])


@router.get(
    "/simulate",
    response_model=GameSimulationResponse,
    summary="Run a single game simulation",
    description="""
    Simulates a complete property trading game with 4 players of different behaviors.

    ## Game Rules:
    - **Board**: 20 properties in sequence
    - **Players**: 4 players with different strategies
    - **Starting Balance**: $300 per player
    - **Win Condition**: Last player with positive balance wins
    - **Maximum Turns**: 1000 (to prevent infinite games)

    ## Player Behaviors:
    1. **Impulsivo (Impulsive)**: Buys every property they land on
    2. **Exigente (Demanding)**: Only buys properties with rent > $50
    3. **Cauteloso (Cautious)**: Only buys if will have $80+ balance remaining
    4. **Aleatório (Random)**: Buys with 50% probability

    ## Game Flow:
    1. Players take turns rolling dice (1-6)
    2. Move forward on the board
    3. Buy property if available and strategy allows
    4. Pay rent if landing on owned property
    5. Go bankrupt if balance becomes negative
    6. Game ends when only one player remains

    ## Returns:
    Complete game results including winner, turn count, and final player statuses.
    """,
    responses={
        200: {
            "description": "Simulation completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "winner": "Impulsivo",
                        "total_turns": 245,
                        "timeout": False,
                        "players": [
                            {
                                "name": "Impulsivo",
                                "behavior": "Impulsivo",
                                "balance": 450,
                                "properties_owned": ["Avenida Paulista", "Copacabana"],
                                "is_active": True,
                                "total_assets": 690,
                            }
                        ],
                        "final_standings": [
                            {
                                "position": 1,
                                "name": "Impulsivo",
                                "balance": 450,
                                "properties_count": 5,
                            }
                        ],
                    }
                }
            },
        }
    },
    tags=["Game Simulation"],
)
async def simulate_game():
    """
    Runs a complete property trading game simulation.

    Executes a full game with 4 AI players using different strategies,
    tracking all moves, purchases, and rent payments until a winner emerges.
    """
    runner = AutoRunner()
    result = runner.run(show_status_every=0)  # Disable periodic status for API

    # Build detailed player responses
    players_response = []
    for player in runner.players:
        players_response.append(
            {
                "name": player.name,
                "behavior": player.behavior.value,
                "balance": player.balance,
                "properties_owned": [prop.name for prop in player.properties_owned],
                "is_active": player.is_active,
                "total_assets": player.get_total_assets(),
            }
        )

    # Build final standings
    standings_response = []
    for i, (name, balance, props_count) in enumerate(result.final_standings, 1):
        standings_response.append(
            {
                "position": i,
                "name": name,
                "balance": balance,
                "properties_count": props_count,
            }
        )

    return {
        "winner": result.winner.name if result.winner else None,
        "total_turns": result.total_turns,
        "timeout": result.timeout,
        "players": players_response,
        "final_standings": standings_response,
    }


@router.get(
    "/simulate/multiple",
    response_model=MultipleSimulationsResponse,
    summary="Run multiple game simulations",
    description="""
    Runs multiple game simulations and returns aggregated statistics.

    Useful for analyzing which player behavior performs best over many games.

    ## Parameters:
    - **simulations**: Number of games to run (1-1000)

    ## Returns:
    Statistical analysis including:
    - Total wins per behavior type
    - Win percentages
    - Average game duration
    - Timeout occurrences
    """,
    responses={
        200: {
            "description": "Multiple simulations completed successfully",
        }
    },
    tags=["Game Simulation"],
)
async def simulate_multiple_games(
    simulations: int = Query(
        default=2,
        ge=1,
        le=10,
        description="Number of simulations to run",
        example=10,
    )
):
    """
    Runs multiple game simulations and returns statistics.

    :param simulations: Number of games to simulate (1-10)
    :type simulations: int
    """
    results = {
        "total_simulations": simulations,
        "wins_by_behavior": {
            "Impulsivo": 0,
            "Exigente": 0,
            "Cauteloso": 0,
            "Aleatório": 0,
        },
        "average_turns": 0,
        "timeout_count": 0,
    }

    total_turns = 0

    for _ in range(simulations):
        runner = AutoRunner()
        result = runner.run(show_status_every=0)

        if result.winner:
            results["wins_by_behavior"][result.winner.name] += 1

        total_turns += result.total_turns

        if result.timeout:
            results["timeout_count"] += 1

    results["average_turns"] = round(total_turns / simulations, 2)

    # Calculate win percentages
    results["win_percentages"] = {
        behavior: round((wins / simulations) * 100, 2)
        for behavior, wins in results["wins_by_behavior"].items()
    }

    return results
