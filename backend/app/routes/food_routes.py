from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.food import FoodItem

router = APIRouter(prefix="/foods", tags=["Foods"])


@router.get("/")
def get_foods(db: Session = Depends(get_db)):
    foods = db.query(FoodItem).order_by(FoodItem.food_name).all()

    return [
        {
            "food_id": food.food_id,
            "food_code": food.food_code,
            "food_name": food.food_name,
            "scientific_name": food.scientific_name,
            "food_group": food.food_group,
            "region": food.region,
            "description": food.description,
        }
        for food in foods
    ]


@router.get("/search")
def search_foods(name: str, db: Session = Depends(get_db)):
    foods = (
        db.query(FoodItem)
        .filter(FoodItem.food_name.ilike(f"%{name}%"))
        .order_by(FoodItem.food_name)
        .all()
    )

    return [
        {
            "food_id": food.food_id,
            "food_code": food.food_code,
            "food_name": food.food_name,
            "scientific_name": food.scientific_name,
            "food_group": food.food_group,
            "region": food.region,
            "description": food.description,
        }
        for food in foods
    ]