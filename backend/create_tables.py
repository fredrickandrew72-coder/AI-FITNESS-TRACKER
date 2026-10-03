from app.database.connection import Base, engine

# Import all models so SQLAlchemy registers their tables
from app.models.user import User
from app.models.food import FoodItem
from app.models.nutrition import NutritionData


Base.metadata.create_all(bind=engine)

print("DATABASE TABLES CREATED SUCCESSFULLY")