import zipfile
import csv
import io
import os


ZIP_PATH = "data/raw/indian_nutrition/ifct2017/compositions-2.0.5.zip"
INDEX_PATH = "ifct2017-compositions-1fcfad7/index.csv"

OUTPUT_DIR = "data/processed"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "indian_food_nutrition.csv")


# Nutrients required by our application
OUTPUT_FIELDS = [
    "food_code",
    "food_name",
    "scientific_name",
    "food_group",
    "region",
    "energy_kcal",
    "protein_g",
    "fat_g",
    "carbohydrate_g",
    "fiber_g",
    "calcium_mg",
    "iron_mg",
    "magnesium_mg",
    "phosphorus_mg",
    "potassium_mg",
    "sodium_mg",
    "zinc_mg",
    "vitamin_a",
    "vitamin_b6",
    "vitamin_c_mg",
    "vitamin_d",
    "folate"
]


def clean_value(value):
    """Clean IFCT values such as 9.20±0.40."""

    if value is None:
        return ""

    value = value.strip()

    if not value:
        return ""

    # Keep only the main value before ±
    if "±" in value:
        value = value.split("±")[0].strip()

    # Handle possible encoding issue
    if "┬▒" in value:
        value = value.split("┬▒")[0].strip()

    try:
        return float(value)
    except ValueError:
        return ""


def get_value(row, column):
    return clean_value(row.get(column, ""))


def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Reading IFCT2017 dataset...")

    with zipfile.ZipFile(ZIP_PATH, "r") as z:

        with z.open(INDEX_PATH) as file:

            text_file = io.TextIOWrapper(
                file,
                encoding="utf-8"
            )

            reader = csv.DictReader(text_file)

            processed_rows = []

            for row in reader:

                processed_row = {
                    "food_code": row.get("code", "").strip(),
                    "food_name": row.get("name", "").strip(),
                    "scientific_name": row.get("scie", "").strip(),
                    "food_group": row.get("grup", "").strip(),
                    "region": row.get("regn", "").strip(),

                    "energy_kcal": round(get_value(row, "enerc") / 4.184, 2),

                    "protein_g": get_value(row, "protcnt"),
                    "fat_g": get_value(row, "fatce"),
                    "carbohydrate_g": get_value(row, "choavldf"),
                    "fiber_g": get_value(row, "fibtg"),

                    "calcium_mg": get_value(row, "ca"),
                    "iron_mg": get_value(row, "fe"),
                    "magnesium_mg": get_value(row, "mg"),
                    "phosphorus_mg": get_value(row, "p"),
                    "potassium_mg": get_value(row, "k"),
                    "sodium_mg": get_value(row, "na"),
                    "zinc_mg": get_value(row, "zn"),

                    "vitamin_a": get_value(row, "vita"),
                    "vitamin_b6": get_value(row, "vitb6c"),
                    "vitamin_c_mg": get_value(row, "vitc"),
                    "vitamin_d": get_value(row, "vitd"),
                    "folate": get_value(row, "folsum"),
                }

                processed_rows.append(processed_row)

    print(f"Foods processed: {len(processed_rows)}")

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=OUTPUT_FIELDS
        )

        writer.writeheader()
        writer.writerows(processed_rows)

    print()
    print("SUCCESS!")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()