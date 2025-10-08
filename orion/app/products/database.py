from sqlalchemy import Column, Float, Integer, String

from orion.core.database.engine import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    base_price = Column(Float, nullable=False)
