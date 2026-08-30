from typing import List, Optional, Dict
from sqlalchemy import text
from contextlib import contextmanager
from database import SessionLocal

@contextmanager
def get_session():
    """
    Контекстный менеджер для сессии SQLAlchemy.
    - Создаёт сессию.
    - При успехе делает commit.
    - При ошибке делает rollback.
    - Всегда закрывает сессию.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_all_items() -> List[Dict]:
    with get_session() as session:
        result = session.execute(
            text("SELECT id, name, price, stock_quantity, description FROM items")
        )
        # dict(row) — самый безопасный способ превратить строку в словарь
        return [dict(row) for row in result.mappings()]


def create_item(name: str, price: float, stock_quantity: int, description: Optional[str] = None) -> Dict:
    with get_session() as session:
        result = session.execute(
            text(
                """
                INSERT INTO items (name, price, stock_quantity, description)
                VALUES (:name, :price, :stock_quantity, :description)
                RETURNING id, name, price, stock_quantity, description
                """
            ),
            {
                "name": name,
                "price": price,
                "stock_quantity": stock_quantity,
                "description": description,
            },
        )
        row = result.mappings().one()
        return dict(row)


def get_item_by_id(item_id: int) -> Optional[dict]:
    with get_session() as session:
        result = session.execute(
            text("SELECT id, name, price, stock_quantity, description FROM items WHERE id = :id"),
            {"id": item_id}
        )
        row = result.mappings().first()
        return dict(row) if row else None
