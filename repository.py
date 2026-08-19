from typing import List, Optional, Dict
from sqlalchemy import text
from database import get_db
from sqlalchemy.orm import Session

def get_all_items() -> List[Dict]:
    session = next(get_db())
    try:
        result = session.execute(
            text("SELECT id, name, price, stock_quantity, description FROM items")
        )
        return [dict(row) for row in result.mappings()]
    finally:
        session.close()


def create_item(
    name: str,
    price: float,
    stock_quantity: int,
    description: Optional[str] = None,
) -> Dict:
    session = next(get_db())
    try:
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
        session.commit()
        row = result.mappings().one()
        return dict(row)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_item_by_id(item_id: int, db: Session) -> Optional[dict]:  # Получаем сессию снаружи
    result = db.execute(
        text("SELECT id, name, price, stock_quantity, description FROM items WHERE id = :id"),
        {"id": item_id},
    )
    row = result.mappings().first()
    return dict(row) if row else None
    # Никаких try/finally, никаких close() — это теперь забота того, кто вызвал функцию