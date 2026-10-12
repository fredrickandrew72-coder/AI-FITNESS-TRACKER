from app.database.connection import Base, engine

# Import all models so SQLAlchemy registers their tables
from app.models.user import User
from app.models.food import FoodItem
from app.models.nutrition import NutritionData
from app.models.food_log import FoodLog
from app.models.recipe_nutrition import RecipeNutrition


Base.metadata.create_all(bind=engine)

print("DATABASE TABLES CREATED SUCCESSFULLY")
