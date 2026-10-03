from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.connection import Base


class NutritionData(Base):
    __tablename__ = "nutrition_data"

    nutrition_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    food_id = Column(
        UUID(as_uuid=True),
        ForeignKey("food_items.food_id"),
        nullable=False
    )

    serving_size_g = Column(Float, nullable=False, default=100.0)

    energy_kcal = Column(Float, nullable=True)

    protein_g = Column(Float, nullable=True)
    fat_g = Column(Float, nullable=True)
    carbohydrate_g = Column(Float, nullable=True)
    fiber_g = Column(Float, nullable=True)

    calcium_mg = Column(Float, nullable=True)
    iron_mg = Column(Float, nullable=True)
    magnesium_mg = Column(Float, nullable=True)
    phosphorus_mg = Column(Float, nullable=True)
    potassium_mg = Column(Float, nullable=True)
    sodium_mg = Column(Float, nullable=True)
    zinc_mg = Column(Float, nullable=True)

    vitamin_a = Column(Float, nullable=True)
    vitamin_b6 = Column(Float, nullable=True)
    vitamin_c_mg = Column(Float, nullable=True)
    vitamin_d = Column(Float, nullable=True)
    folate = Column(Float, nullable=True)

    source = Column(String(100), nullable=False, default="IFCT2017")