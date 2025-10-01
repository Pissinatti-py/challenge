from typing import List, Optional
from pydantic import BaseModel, Field

from src.schemas.player_response import PlayerResponse
from src.schemas.final_standing_response import FinalStanding


class GameSimulationResponse(BaseModel):
    """Complete game simulation results"""

    winner: Optional[str] = Field(
        None, description="Name of the winning player", example="Impulsivo"
    )
    total_turns: int = Field(
        ..., description="Total number of turns played", example=245
    )
    timeout: bool = Field(
        ..., description="Whether game ended due to timeout", example=False
    )
    players: List[PlayerResponse] = Field(
        ..., description="Final status of all players"
    )
    final_standings: List[FinalStanding] = Field(
        ..., description="Final rankings sorted by performance"
    )

    class Config:
        json_schema_extra = {
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
                    },
                    {
                        "name": "Exigente",
                        "behavior": "Exigente",
                        "balance": -20,
                        "properties_owned": [],
                        "is_active": False,
                        "total_assets": -20,
                    },
                ],
                "final_standings": [
                    {
                        "position": 1,
                        "name": "Impulsivo",
                        "balance": 450,
                        "properties_count": 5,
                    },
                    {
                        "position": 2,
                        "name": "Cauteloso",
                        "balance": 120,
                        "properties_count": 2,
                    },
                ],
            }
        }
