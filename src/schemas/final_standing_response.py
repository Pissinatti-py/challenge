from pydantic import BaseModel, Field


class FinalStanding(BaseModel):
    """Final game standings"""

    position: int = Field(..., description="Final position (1st, 2nd, etc)", example=1)
    name: str = Field(..., description="Player name", example="Impulsivo")
    balance: int = Field(..., description="Final balance", example=450)
    properties_count: int = Field(
        ..., description="Number of properties owned", example=5
    )
