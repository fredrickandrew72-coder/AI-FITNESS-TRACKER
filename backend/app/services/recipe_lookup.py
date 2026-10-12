from sqlalchemy.orm import Session

from app.models.food import FoodItem
from app.models.recipe_nutrition import RecipeNutrition


def get_recipe_by_code(
    db: Session,
    food_code: str
):
    food = (
        db.query(FoodItem)
        .filter(FoodItem.food_code == food_code)
        .first()
    )

    if not food:
        return None

    nutrition = (
        db.query(RecipeNutrition)
        .filter(RecipeNutrition.food_id == food.food_id)
        .first()
    )

    if not nutrition:
        return None

    return {
        "food_id": food.food_id,
        "food_code": food.food_code,
        "food_name": food.food_name,
        "serving_unit": nutrition.serving_unit,
        "energy_kcal": nutrition.energy_kcal,
        "protein_g": nutrition.protein_g,
        "carbohydrate_g": nutrition.carbohydrate_g,
        "fat_g": nutrition.fat_g,
        "fiber_g": nutrition.fiber_g,
        "serving_energy_kcal": nutrition.serving_energy_kcal,
        "serving_protein_g": nutrition.serving_protein_g,
        "serving_carbohydrate_g": nutrition.serving_carbohydrate_g,
        "serving_fat_g": nutrition.serving_fat_g,
        "serving_fiber_g": nutrition.serving_fiber_g,
        "source": nutrition.source,
    }
