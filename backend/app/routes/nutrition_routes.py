from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.food_log import FoodLog
from app.models.food import FoodItem
from app.models.nutrition import NutritionData
from app.models.recipe_nutrition import RecipeNutrition
from app.schemas.food_log_nutrition import (
    FoodLogNutritionResponse,
    NutritionResponse,
)


router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.get(
    "/food-log/{log_id}",
    response_model=FoodLogNutritionResponse
)
def get_food_log_nutrition(
    log_id: str,
    db: Session = Depends(get_db)
):
    food_log = (
        db.query(FoodLog)
        .filter(FoodLog.log_id == log_id)
        .first()
    )

    if not food_log:
        raise HTTPException(
            status_code=404,
            detail="Food log not found"
        )

    food = (
        db.query(FoodItem)
        .filter(FoodItem.food_id == food_log.food_id)
        .first()
    )

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    nutrition = (
        db.query(NutritionData)
        .filter(NutritionData.food_id == food_log.food_id)
        .first()
    )

    if not nutrition:
        recipe = (
            db.query(RecipeNutrition)
            .filter(RecipeNutrition.food_id == food_log.food_id)
            .first()
        )

        if not recipe:
            raise HTTPException(
                status_code=404,
                detail="Nutrition data not found"
            )

        multiplier = food_log.quantity_g / 100.0

        return FoodLogNutritionResponse(
            log_id=food_log.log_id,
            food_id=food.food_id,
            food_name=food.food_name,
            quantity_g=food_log.quantity_g,
            energy_kcal=recipe.energy_kcal * multiplier if recipe.energy_kcal is not None else None,
            protein_g=recipe.protein_g * multiplier if recipe.protein_g is not None else None,
            fat_g=recipe.fat_g * multiplier if recipe.fat_g is not None else None,
            carbohydrate_g=recipe.carbohydrate_g * multiplier if recipe.carbohydrate_g is not None else None,
            fiber_g=recipe.fiber_g * multiplier if recipe.fiber_g is not None else None,
            source=recipe.source,
        )

    multiplier = food_log.quantity_g / nutrition.serving_size_g

    return FoodLogNutritionResponse(
        log_id=food_log.log_id,
        food_id=food.food_id,
        food_name=food.food_name,
        quantity_g=food_log.quantity_g,

        energy_kcal=(
            nutrition.energy_kcal * multiplier
            if nutrition.energy_kcal is not None else None
        ),
        protein_g=(
            nutrition.protein_g * multiplier
            if nutrition.protein_g is not None else None
        ),
        fat_g=(
            nutrition.fat_g * multiplier
            if nutrition.fat_g is not None else None
        ),
        carbohydrate_g=(
            nutrition.carbohydrate_g * multiplier
            if nutrition.carbohydrate_g is not None else None
        ),
        fiber_g=(
            nutrition.fiber_g * multiplier
            if nutrition.fiber_g is not None else None
        ),

        calcium_mg=(
            nutrition.calcium_mg * multiplier
            if nutrition.calcium_mg is not None else None
        ),
        iron_mg=(
            nutrition.iron_mg * multiplier
            if nutrition.iron_mg is not None else None
        ),
        magnesium_mg=(
            nutrition.magnesium_mg * multiplier
            if nutrition.magnesium_mg is not None else None
        ),
        phosphorus_mg=(
            nutrition.phosphorus_mg * multiplier
            if nutrition.phosphorus_mg is not None else None
        ),
        potassium_mg=(
            nutrition.potassium_mg * multiplier
            if nutrition.potassium_mg is not None else None
        ),
        sodium_mg=(
            nutrition.sodium_mg * multiplier
            if nutrition.sodium_mg is not None else None
        ),
        zinc_mg=(
            nutrition.zinc_mg * multiplier
            if nutrition.zinc_mg is not None else None
        ),

        vitamin_a=(
            nutrition.vitamin_a * multiplier
            if nutrition.vitamin_a is not None else None
        ),
        vitamin_b6=(
            nutrition.vitamin_b6 * multiplier
            if nutrition.vitamin_b6 is not None else None
        ),
        vitamin_c_mg=(
            nutrition.vitamin_c_mg * multiplier
            if nutrition.vitamin_c_mg is not None else None
        ),
        vitamin_d=(
            nutrition.vitamin_d * multiplier
            if nutrition.vitamin_d is not None else None
        ),
        folate=(
            nutrition.folate * multiplier
            if nutrition.folate is not None else None
        ),

        source=nutrition.source
    )
@router.get("/food/{food_id}", response_model=NutritionResponse)
def get_food_nutrition(food_id: str, db: Session = Depends(get_db)):
    food = db.query(FoodItem).filter(FoodItem.food_id == food_id).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    nutrition = (
        db.query(NutritionData)
        .filter(NutritionData.food_id == food_id)
        .first()
    )

    if not nutrition:
        raise HTTPException(status_code=404, detail="Nutrition data not found")

    return NutritionResponse(
        food_id=food.food_id,
        food_name=food.food_name,
        serving_size_g=nutrition.serving_size_g,
        energy_kcal=nutrition.energy_kcal,
        protein_g=nutrition.protein_g,
        fat_g=nutrition.fat_g,
        carbohydrate_g=nutrition.carbohydrate_g,
        fiber_g=nutrition.fiber_g,
        calcium_mg=nutrition.calcium_mg,
        iron_mg=nutrition.iron_mg,
        magnesium_mg=nutrition.magnesium_mg,
        phosphorus_mg=nutrition.phosphorus_mg,
        potassium_mg=nutrition.potassium_mg,
        sodium_mg=nutrition.sodium_mg,
        zinc_mg=nutrition.zinc_mg,
        vitamin_a=nutrition.vitamin_a,
        vitamin_b6=nutrition.vitamin_b6,
        vitamin_c_mg=nutrition.vitamin_c_mg,
        vitamin_d=nutrition.vitamin_d,
        folate=nutrition.folate,
        source=nutrition.source,
    )
