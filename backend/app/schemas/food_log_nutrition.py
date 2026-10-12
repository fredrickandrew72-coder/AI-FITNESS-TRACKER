from uuid import UUID

from pydantic import BaseModel


class FoodLogNutritionResponse(BaseModel):
    log_id: UUID
    food_id: UUID
    food_name: str
    quantity_g: float

    energy_kcal: float | None = None
    protein_g: float | None = None
    fat_g: float | None = None
    carbohydrate_g: float | None = None
    fiber_g: float | None = None

    calcium_mg: float | None = None
    iron_mg: float | None = None
    magnesium_mg: float | None = None
    phosphorus_mg: float | None = None
    potassium_mg: float | None = None
    sodium_mg: float | None = None
    zinc_mg: float | None = None

    vitamin_a: float | None = None
    vitamin_b6: float | None = None
    vitamin_c_mg: float | None = None
    vitamin_d: float | None = None
    folate: float | None = None

    source: str
class NutritionResponse(BaseModel):
    food_id: UUID
    food_name: str
    serving_size_g: float

    energy_kcal: float | None = None
    protein_g: float | None = None
    fat_g: float | None = None
    carbohydrate_g: float | None = None
    fiber_g: float | None = None

    calcium_mg: float | None = None
    iron_mg: float | None = None
    magnesium_mg: float | None = None
    phosphorus_mg: float | None = None
    potassium_mg: float | None = None
    sodium_mg: float | None = None
    zinc_mg: float | None = None

    vitamin_a: float | None = None
    vitamin_b6: float | None = None
    vitamin_c_mg: float | None = None
    vitamin_d: float | None = None
    folate: float | None = None

    source: str