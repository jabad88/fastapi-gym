from db import Base
from sqlalchemy import Column, Integer, String

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    reps = Column(Integer, nullable=False)
