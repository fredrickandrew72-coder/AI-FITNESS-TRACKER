from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.connection import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    food_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    food_code = Column(String(20), unique=True, nullable=False, index=True)
    food_name = Column(String(255), nullable=False, index=True)

    scientific_name = Column(String(255), nullable=True)
    food_group = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)

    description = Column(Text, nullable=True)