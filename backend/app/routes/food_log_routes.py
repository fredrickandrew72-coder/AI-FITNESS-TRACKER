from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.food_log import FoodLog
from app.models.user import User
from app.models.food import FoodItem
from app.schemas.food_log import FoodLogCreate, FoodLogResponse


router = APIRouter(prefix="/food-logs", tags=["Food Logs"])


@router.post("/", response_model=FoodLogResponse)
def create_food_log(
    log_data: FoodLogCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == log_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    food = db.query(FoodItem).filter(FoodItem.food_id == log_data.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    food_log = FoodLog(
        user_id=log_data.user_id,
        food_id=log_data.food_id,
        quantity_g=log_data.quantity_g,
        meal_type=log_data.meal_type,
        input_method=log_data.input_method
    )

    db.add(food_log)
    db.commit()
    db.refresh(food_log)

    return food_log


@router.get("/{user_id}", response_model=list[FoodLogResponse])
def get_user_food_logs(
    user_id,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return (
        db.query(FoodLog)
        .filter(FoodLog.user_id == user_id)
        .order_by(FoodLog.logged_at.desc())
        .all()
    )
