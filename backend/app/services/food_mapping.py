FOOD_CLASS_TO_CODE = {
    "Aloo Paratha": "ASC098",
    "Rasgulla": "BFP392",
    "Palak Paneer": "ASC215",
    "Poha": "BFP044",
    "Khichdi": "BFP144",
    "Omelette": "ASC061",
    "Plain Rice": "ASC113",
    "Chapati": "ASC096",
}

AMBIGUOUS_FOOD_CLASSES = {
    "Biryani": {
        "message": "Biryani type is required. Please specify mutton or vegetable biryani.",
        "options": ["Mutton Biryani", "Vegetable Biryani"],
        "food_codes": {
            "Mutton Biryani": "ASC122",
            "Vegetable Biryani": "ASC123",
        },
    },
}

MANUAL_FALLBACK_CLASSES = {
    "Chicken Tikka": {
        "message": "Chicken Tikka was detected, but no suitable nutrition record is available in the current INDB database. Please enter the food details manually."
    }
}


def get_food_code(class_name: str):
    return FOOD_CLASS_TO_CODE.get(class_name)


def get_ambiguous_food_info(class_name: str):
    return AMBIGUOUS_FOOD_CLASSES.get(class_name)


def get_manual_fallback_info(class_name: str):
    return MANUAL_FALLBACK_CLASSES.get(class_name)
