-- 1. Создаём таблицы (нормализованная схема)

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0,
    stock_quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    total_price NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'new',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 1,
    unit_price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_order_item UNIQUE (order_id, item_id)
);

-- 2. Добавляем индексы (по плану 40–80 мин)
CREATE INDEX idx_order_items_item_id ON order_items(item_id);
-- Зачем: быстро искать все позиции заказа по товару (например, «где встречается товар X»)

CREATE INDEX idx_orders_created_at ON orders(created_at);
-- Зачем: сортировка и фильтрация по дате (новые заказы, отчёты за период)

CREATE INDEX idx_orders_total_price ON orders(total_price);
-- Зачем: поиск по сумме (дорогие/дешёвые заказы), отчёты по диапазонам цен

-- 3. Наполняем тестовыми данными (seed)
INSERT INTO items (name, price, stock_quantity) VALUES
('Кроссовки Nike', 9990.00, 15),
('Футболка базовая', 1990.00, 50),
('Кепка спортивная', 2490.00, 30),
('Шорты летние', 3290.00, 20);

INSERT INTO orders (customer_name, total_price, status) VALUES
('Иван Иванов', 11980.00, 'new'),
('Анна Петрова', 5780.00, 'paid'),
('Сергей Сидоров', 13280.00, 'shipping');

INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES
(1, 1, 1, 9990.00),
(1, 2, 1, 1990.00),
(2, 2, 2, 1990.00),
(2, 4, 1, 3290.00),
(3, 1, 1, 9990.00),
(3, 3, 1, 2490.00),
(3, 4, 1, 3290.00);
