from typing import List
from pydantic import BaseModel, Field


class PlayerResponse(BaseModel):
    """Player status in the response"""

    name: str = Field(..., description="Player name", example="Impulsivo")
    behavior: str = Field(..., description="Player behavior type", example="Impulsivo")
    balance: int = Field(..., description="Current balance", example=450)
    properties_owned: List[str] = Field(
        default=[],
        description="List of owned property names",
        example=["Avenida Paulista", "Copacabana"],
    )
    is_active: bool = Field(
        ..., description="Whether player is still in game", example=True
    )
    total_assets: int = Field(
        ..., description="Total assets (balance + properties value)", example=690
    )
