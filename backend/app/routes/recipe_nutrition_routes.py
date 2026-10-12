from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.food import FoodItem
from app.models.recipe_nutrition import RecipeNutrition
from app.schemas.recipe_nutrition import RecipeNutritionResponse


router = APIRouter(prefix="/recipe-nutrition", tags=["Recipe Nutrition"])


@router.get("/{food_id}", response_model=RecipeNutritionResponse)
def get_recipe_nutrition(
    food_id: str,
    db: Session = Depends(get_db)
):
    food = (
        db.query(FoodItem)
        .filter(FoodItem.food_id == food_id)
        .first()
    )

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    nutrition = (
        db.query(RecipeNutrition)
        .filter(RecipeNutrition.food_id == food_id)
        .first()
    )

    if not nutrition:
        raise HTTPException(
            status_code=404,
            detail="Recipe nutrition data not found"
        )

    return RecipeNutritionResponse(
        food_id=food.food_id,
        food_name=food.food_name,
        serving_unit=nutrition.serving_unit,

        energy_kcal=nutrition.energy_kcal,
        protein_g=nutrition.protein_g,
        carbohydrate_g=nutrition.carbohydrate_g,
        fat_g=nutrition.fat_g,
        fiber_g=nutrition.fiber_g,

        serving_energy_kcal=nutrition.serving_energy_kcal,
        serving_protein_g=nutrition.serving_protein_g,
        serving_carbohydrate_g=nutrition.serving_carbohydrate_g,
        serving_fat_g=nutrition.serving_fat_g,
        serving_fiber_g=nutrition.serving_fiber_g,

        source=nutrition.source
    )
