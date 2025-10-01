from pydantic import BaseModel, Field


class MultipleSimulationsResponse(BaseModel):
    """Response for multiple game simulations with statistics"""

    total_simulations: int = Field(
        ..., description="Total number of games simulated", example=100
    )
    wins_by_behavior: dict = Field(
        ..., description="Number of wins for each behavior type"
    )
    win_percentages: dict = Field(
        ..., description="Win percentage for each behavior type"
    )
    average_turns: float = Field(
        ..., description="Average number of turns per game", example=245.5
    )
    timeout_count: int = Field(
        ..., description="Number of games that reached timeout", example=2
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total_simulations": 100,
                "wins_by_behavior": {
                    "Impulsivo": 45,
                    "Exigente": 20,
                    "Cauteloso": 25,
                    "Aleatório": 10,
                },
                "win_percentages": {
                    "Impulsivo": 45.0,
                    "Exigente": 20.0,
                    "Cauteloso": 25.0,
                    "Aleatório": 10.0,
                },
                "average_turns": 245.5,
                "timeout_count": 2,
            }
        }
