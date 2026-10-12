from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FoodLogCreate(BaseModel):
    user_id: UUID
    food_id: UUID
    quantity_g: float = Field(gt=0)
    meal_type: str | None = None
    input_method: str = "text"


class FoodLogResponse(BaseModel):
    log_id: UUID
    user_id: UUID
    food_id: UUID
    quantity_g: float
    meal_type: str | None
    input_method: str
    logged_at: datetime

    model_config = {"from_attributes": True}
