import json
from typing import List, Optional


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class Library:
    def __init__(self, storage_file: str = "books.json"):
        self.storage_file = storage_file
        self.books: List[Book] = self._load_books()

    def _load_books(self) -> List[Book]:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_books(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id=new_id, title=title, author=author, year=year)
        self.books.append(new_book)
        self._save_books()
        print(f"Книга добавлена: {new_book.title} (ID: {new_book.id})")

    def remove_book(self, book_id: int):
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self._save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, query: str) -> List[Book]:
        return [
            book
            for book in self.books
            if query.lower() in book.title.lower()
               or query.lower() in book.author.lower()
               or query == str(book.year)
        ]

    def display_books(self):
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(
                f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
            )

    def update_status(self, book_id: int, new_status: str):
        book = self.find_book_by_id(book_id)
        if book:
            book.status = new_status
            self._save_books()
            print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = int(input("Введите год издания: ").strip())
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: ").strip())
            library.remove_book(book_id)
        elif choice == "3":
            query = input("Введите запрос для поиска (название, автор или год): ").strip()
            results = library.search_books(query)
            if results:
                for book in results:
                    print(
                        f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
                    )
            else:
                print("Книги не найдены.")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: ").strip())
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
            library.update_status(book_id, new_status)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие из меню.")


if __name__ == "__main__":
    main()
