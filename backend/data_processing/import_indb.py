import csv
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database.connection import SessionLocal
from app.models.food import FoodItem
from app.models.recipe_nutrition import RecipeNutrition


CSV_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "processed",
        "indian_recipe_nutrition.csv",
    )
)


def clean_float(value):
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def import_recipes():
    print("Reading INDB processed CSV...")
    print(f"CSV path: {CSV_PATH}")

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"CSV file not found: {CSV_PATH}"
        )

    db = SessionLocal()

    try:
        with open(
            CSV_PATH,
            "r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            imported = 0
            skipped = 0
            foods_created = 0

            for row in reader:

                food_code = row["food_code"].strip()
                food_name = row["food_name"].strip()

                if not food_code or not food_name:
                    skipped += 1
                    continue

                # Find existing food by food code
                food = (
                    db.query(FoodItem)
                    .filter(FoodItem.food_code == food_code)
                    .first()
                )

                # Create FoodItem if it does not exist
                if not food:
                    food = FoodItem(
                        food_code=food_code,
                        food_name=food_name,
                        food_group="Prepared Food",
                        region=None,
                        scientific_name=None,
                    )

                    db.add(food)
                    db.flush()

                    foods_created += 1

                # Prevent duplicate recipe nutrition records
                existing_recipe = (
                    db.query(RecipeNutrition)
                    .filter(
                        RecipeNutrition.food_id == food.food_id
                    )
                    .first()
                )

                if existing_recipe:
                    skipped += 1
                    continue

                recipe = RecipeNutrition(
                    food_id=food.food_id,

                    serving_unit=(
                        row["servings_unit"].strip()
                        if row["servings_unit"]
                        else None
                    ),

                    energy_kcal=clean_float(
                        row["energy_kcal"]
                    ),
                    protein_g=clean_float(
                        row["protein_g"]
                    ),
                    carbohydrate_g=clean_float(
                        row["carb_g"]
                    ),
                    fat_g=clean_float(
                        row["fat_g"]
                    ),
                    fiber_g=clean_float(
                        row["fibre_g"]
                    ),

                    serving_energy_kcal=clean_float(
                        row["unit_serving_energy_kcal"]
                    ),
                    serving_protein_g=clean_float(
                        row["unit_serving_protein_g"]
                    ),
                    serving_carbohydrate_g=clean_float(
                        row["unit_serving_carb_g"]
                    ),
                    serving_fat_g=clean_float(
                        row["unit_serving_fat_g"]
                    ),
                    serving_fiber_g=clean_float(
                        row["unit_serving_fibre_g"]
                    ),

                    source="INDB",
                )

                db.add(recipe)
                imported += 1

                if imported % 100 == 0:
                    db.commit()
                    print(f"Imported recipe nutrition: {imported}")

            db.commit()

            print()
            print("INDB IMPORT SUCCESSFUL")
            print(f"Recipe nutrition imported: {imported}")
            print(f"Food items created: {foods_created}")
            print(f"Rows skipped: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_recipes()
