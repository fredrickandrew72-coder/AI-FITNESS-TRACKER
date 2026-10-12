from pathlib import Path
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.food_detection import detect_food
from app.services.food_mapping import (
    get_food_code,
    get_ambiguous_food_info,
    get_manual_fallback_info,
)
from app.services.recipe_lookup import get_recipe_by_code


router = APIRouter(prefix="/food-detection", tags=["Food Detection"])


@router.post("/")
async def detect_food_from_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file"
        )

    suffix = Path(file.filename or "").suffix.lower()

    if not suffix:
        suffix = ".jpg"

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        detections = detect_food(temp_path)

        if not detections:
            return {
                "detected": False,
                "message": "Food could not be identified confidently. Please enter what you ate.",
                "detections": []
            }

        best_detection = detections[0]
        class_name = best_detection["class_name"]

        ambiguous_info = get_ambiguous_food_info(class_name)

        if ambiguous_info:
            return {
                "detected": True,
                "food_name": class_name,
                "confidence": best_detection["confidence"],
                "requires_clarification": True,
                "message": ambiguous_info["message"],
                "options": ambiguous_info["options"],
                "detections": detections
            }

        fallback_info = get_manual_fallback_info(class_name)

        if fallback_info:
            return {
                "detected": True,
                "food_name": class_name,
                "confidence": best_detection["confidence"],
                "requires_manual_input": True,
                "message": fallback_info["message"],
                "detections": detections
            }

        food_code = get_food_code(class_name)

        if not food_code:
            return {
                "detected": True,
                "food_name": class_name,
                "confidence": best_detection["confidence"],
                "requires_manual_input": True,
                "message": "Food was detected, but no nutrition mapping is available. Please enter the food manually.",
                "detections": detections
            }

        recipe = get_recipe_by_code(db, food_code)

        if not recipe:
            return {
                "detected": True,
                "food_name": class_name,
                "confidence": best_detection["confidence"],
                "requires_manual_input": True,
                "message": "Nutrition data could not be found for the detected food. Please enter the food manually.",
                "detections": detections
            }

        return {
            "detected": True,
            "food_name": class_name,
            "confidence": best_detection["confidence"],
            "food_code": recipe["food_code"],
            "food_id": recipe["food_id"],
            "nutrition": {
                "serving_unit": recipe["serving_unit"],
                "energy_kcal": recipe["energy_kcal"],
                "protein_g": recipe["protein_g"],
                "carbohydrate_g": recipe["carbohydrate_g"],
                "fat_g": recipe["fat_g"],
                "fiber_g": recipe["fiber_g"],
                "serving_energy_kcal": recipe["serving_energy_kcal"],
                "serving_protein_g": recipe["serving_protein_g"],
                "serving_carbohydrate_g": recipe["serving_carbohydrate_g"],
                "serving_fat_g": recipe["serving_fat_g"],
                "serving_fiber_g": recipe["serving_fiber_g"],
                "source": recipe["source"],
            },
            "detections": detections
        }

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)


@router.get("/biryani/{biryani_type}")
def get_biryani_nutrition(
    biryani_type: str,
    db: Session = Depends(get_db)
):
    biryani_options = {
        "mutton": "ASC122",
        "vegetable": "ASC123",
    }

    food_code = biryani_options.get(biryani_type.lower())

    if not food_code:
        raise HTTPException(
            status_code=400,
            detail="Invalid biryani type. Choose mutton or vegetable."
        )

    recipe = get_recipe_by_code(db, food_code)

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Biryani nutrition data not found"
        )

    return {
        "food_name": recipe["food_name"],
        "food_code": recipe["food_code"],
        "food_id": recipe["food_id"],
        "nutrition": {
            "serving_unit": recipe["serving_unit"],
            "energy_kcal": recipe["energy_kcal"],
            "protein_g": recipe["protein_g"],
            "carbohydrate_g": recipe["carbohydrate_g"],
            "fat_g": recipe["fat_g"],
            "fiber_g": recipe["fiber_g"],
            "serving_energy_kcal": recipe["serving_energy_kcal"],
            "serving_protein_g": recipe["serving_protein_g"],
            "serving_carbohydrate_g": recipe["serving_carbohydrate_g"],
            "serving_fat_g": recipe["serving_fat_g"],
            "serving_fiber_g": recipe["serving_fiber_g"],
            "source": recipe["source"],
        }
    }
