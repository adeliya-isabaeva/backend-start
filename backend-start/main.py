# import sys
# print("Проект запущен. День 1.")
# print("Путь к интерпретатору:", sys.executable)
# print("Проверка коммита")
books = [
    {"title": "Война и мир", "author": "Толстой", "pages": 1225},
    {"title": "Преступление и наказание", "author": "Достоевский", "pages": 672},
    {"title": "Анна Каренина", "author": "Толстой", "pages": 864},
    {"title": "Отцы и дети", "author": "Тургенев", "pages": 288},
    {"title": "Мёртвые души", "author": "Гоголь", "pages": 352},
]
def show_books(book_list):
    for book in book_list:
        print(f"{book['title']} — {book['author']}")

# Вызываем функцию
show_books(books)


