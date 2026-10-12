from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.connection import Base


class RecipeNutrition(Base):
    __tablename__ = "recipe_nutrition"

    recipe_nutrition_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    food_id = Column(
        UUID(as_uuid=True),
        ForeignKey("food_items.food_id"),
        nullable=False,
        index=True
    )

    serving_unit = Column(String(100), nullable=True)

    energy_kcal = Column(Float, nullable=True)
    protein_g = Column(Float, nullable=True)
    carbohydrate_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    fiber_g = Column(Float, nullable=True)

    serving_energy_kcal = Column(Float, nullable=True)
    serving_protein_g = Column(Float, nullable=True)
    serving_carbohydrate_g = Column(Float, nullable=True)
    serving_fat_g = Column(Float, nullable=True)
    serving_fiber_g = Column(Float, nullable=True)

    source = Column(
        String(100),
        nullable=False,
        default="INDB"
    )
