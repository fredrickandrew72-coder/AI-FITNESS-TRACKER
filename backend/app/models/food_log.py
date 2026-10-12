import uuid
from datetime import datetime

from sqlalchemy import Column, Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class FoodLog(Base):
    __tablename__ = "food_logs"

    log_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )

    food_id = Column(
        UUID(as_uuid=True),
        ForeignKey("food_items.food_id"),
        nullable=False,
        index=True
    )

    quantity_g = Column(
        Float,
        nullable=False
    )

    meal_type = Column(
        String(30),
        nullable=True
    )

    input_method = Column(
        String(20),
        nullable=False,
        default="text"
    )

    logged_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
