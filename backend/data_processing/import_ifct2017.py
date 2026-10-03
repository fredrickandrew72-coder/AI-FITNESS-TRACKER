import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
import csv

from app.database.connection import SessionLocal
from app.models.food import FoodItem
from app.models.nutrition import NutritionData


# Project-level processed dataset
CSV_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "processed",
        "indian_food_nutrition.csv",
    )
)


def clean_float(value):
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def import_foods():

    print("Reading IFCT2017 processed CSV...")
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

            for row in reader:

                food_code = row["food_code"].strip()

                if not food_code:
                    skipped += 1
                    continue

                # Prevent duplicate imports
                existing_food = (
                    db.query(FoodItem)
                    .filter(FoodItem.food_code == food_code)
                    .first()
                )

                if existing_food:
                    skipped += 1
                    continue

                # -------------------------
                # Food table
                # -------------------------

                food = FoodItem(
                    food_code=food_code,
                    food_name=row["food_name"].strip(),
                    scientific_name=row["scientific_name"].strip() or None,
                    food_group=row["food_group"].strip() or None,
                    region=row["region"].strip() or None,
                )

                db.add(food)

                # Flush so PostgreSQL/SQLAlchemy generates food_id
                db.flush()

                # -------------------------
                # Nutrition table
                # -------------------------

                nutrition = NutritionData(
                    food_id=food.food_id,

                    serving_size_g=100.0,

                    energy_kcal=clean_float(row["energy_kcal"]),

                    protein_g=clean_float(row["protein_g"]),
                    fat_g=clean_float(row["fat_g"]),
                    carbohydrate_g=clean_float(
                        row["carbohydrate_g"]
                    ),
                    fiber_g=clean_float(row["fiber_g"]),

                    calcium_mg=clean_float(row["calcium_mg"]),
                    iron_mg=clean_float(row["iron_mg"]),
                    magnesium_mg=clean_float(
                        row["magnesium_mg"]
                    ),
                    phosphorus_mg=clean_float(
                        row["phosphorus_mg"]
                    ),
                    potassium_mg=clean_float(
                        row["potassium_mg"]
                    ),
                    sodium_mg=clean_float(row["sodium_mg"]),
                    zinc_mg=clean_float(row["zinc_mg"]),

                    vitamin_a=clean_float(row["vitamin_a"]),
                    vitamin_b6=clean_float(row["vitamin_b6"]),
                    vitamin_c_mg=clean_float(
                        row["vitamin_c_mg"]
                    ),
                    vitamin_d=clean_float(row["vitamin_d"]),
                    folate=clean_float(row["folate"]),

                    source="IFCT2017",
                )

                db.add(nutrition)

                imported += 1

                # Commit periodically
                if imported % 100 == 0:
                    db.commit()
                    print(f"Imported: {imported}")

            db.commit()

            print()
            print("IMPORT SUCCESSFUL")
            print(f"Foods imported: {imported}")
            print(f"Rows skipped: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_foods()