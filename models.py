from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Target(Base):
    __tablename__ = "Target"

    id = Column(Integer, primary_key=True)
    target = Column(String, nullable=False)
    value = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)


class Drug(Base):
    __tablename__ = "Drug"

    id = Column(Integer, primary_key=True)
    drug = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)