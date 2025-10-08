from sqlalchemy import Column, Integer, String

from orion.core.database.engine import Base


class Task(Base):
    __tablename__ = "tasks"

    # Define your columns here
    # For example:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
