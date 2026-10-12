from uuid import UUID

from pydantic import BaseModel


class RecipeNutritionResponse(BaseModel):
    food_id: UUID
    food_name: str
    serving_unit: str | None = None

    energy_kcal: float | None = None
    protein_g: float | None = None
    carbohydrate_g: float | None = None
    fat_g: float | None = None
    fiber_g: float | None = None

    serving_energy_kcal: float | None = None
    serving_protein_g: float | None = None
    serving_carbohydrate_g: float | None = None
    serving_fat_g: float | None = None
    serving_fiber_g: float | None = None

    source: str
