from typing import List, Optional, Dict
from sqlalchemy import text
from database import get_session  # <-- Только это

def get_all_items() -> List[Dict]:
    """
        Получает все товары из таблицы items.

        Returns:
            List[Dict]: Список словарей с данными о товарах.
        """
    with get_session() as session:
        result = session.execute(text("SELECT id, name, price, stock_quantity, description FROM items"))
        return [row._asdict() for row in result.mappings()]

def create_item(name: str, price: float, stock_quantity: int, description: Optional[str] = None) -> Dict:
    """
        Создаёт новый товар в базе данных.

        Args:
            name (str): Название товара.
            price (float): Цена товара.
            stock_quantity (int): Количество на складе.
            description (Optional[str]): Описание товара.

        Returns:
            Dict: Словарь с данными созданного товара (включая присвоенный ID).
        """
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
        session.commit()
        row = result.mappings().one()
        return dict(row)


def get_item_by_id(item_id: int) -> Optional[dict]:
    """
        Находит товар по его уникальному идентификатору.

        Args:
            item_id (int): ID товара.

        Returns:
            Optional[Dict]: Словарь с данными товара или None, если товар не найден.
        """
    from database import get_session
    from sqlalchemy import text

    with get_session() as session:
        result = session.execute(
            text("SELECT id, name, price, stock_quantity, description FROM items WHERE id = :id"),
            {"id": item_id}
        )
        row = result.mappings().first()
        return dict(row) if row else None
