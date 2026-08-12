from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# Это "фундамент", от которого наследуются все таблицы.
# Alembic будет смотреть именно сюда.
Base = declarative_base()

class Item(Base):
    # Имя таблицы, которая появится в PostgreSQL
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=True)
