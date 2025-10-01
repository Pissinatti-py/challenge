from pydantic import BaseModel, Field


class PropertyResponse(BaseModel):
    """Property information in the response"""

    name: str = Field(..., description="Property name", example="Avenida Paulista")
    sale_cost: int = Field(..., description="Property purchase cost", example=120)
    rent_value: int = Field(
        ..., description="Rent value when landing on property", example=12
    )
