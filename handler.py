"""Handlers of the main operations in the Library."""

import json
import uuid

from config_log import get_logger
from models import Book, BookStatus

logger = get_logger(__name__)


class Library:
    """Library class."""

    def __init__(self, storage_path: str) -> None:
        """Initialize the Library class."""
        self.storage = storage_path
        logger.info(f"Library initialized with storage in {self.storage}")

    def _read_storage(self) -> dict:
        """Read the storage file."""
        with open(self.storage, "r", encoding="utf-8") as file:
            data: dict[str, list] = json.load(file)

        logger.info("The storage was successfully read.")
        return data

    def _write_storage(self, data: dict) -> None:
        """Write the storage file."""
        with open(self.storage, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        logger.info("The storage was successfully write.")

    def _get_books(self) -> tuple[dict, list] | None:
        """Get all books from the library."""
        book_data: dict = self._read_storage()
        books: list = book_data["books"]

        if not books:
            print("\nВ Библиотеке сейчас нет книг!")
            logger.info("Books was not get, because storage is empty.")
            return None

        logger.info("Books was successfully get.")
        return book_data, books

    def create(self) -> None:
        """Add a book to the library."""
        print("\nЗапускаем добавление книги в Библиотеку")

        title: str = input("\nВведите название книги: ")
        author: str = input("\nВведите автора книги: ")
        while True:
            try:
                year: int = int(input("\nВведите год публикации книги: "))
            except ValueError:
                logger.warning("Year is not int while Book creating.")
                print("\nГод публикации должен быть числом!")
            else:
                break

        print(
            f'Вы действительно хотите добавить книгу "{title}", '
            f"написанную автором {author} в {year} году?"
        )

        command: str = input("1: Создать книгу\n2: Отмена\n")
        while command not in ["1", "2"]:
            print("\nКоманда не найдена!")
            command = input("1: Создать книгу\n2: Отмена\n")

        if command == "2":
            print("\nКнига не добавлена в библиотеку!")
            return

        existing_data: dict = self._read_storage()
        new_book: Book = Book(
            id=uuid.uuid4(),
            title=title,
            author=author,
            year=year,
        )
        existing_data["books"].append(new_book.as_dict)
        self._write_storage(existing_data)
        logger.info(f"Book {new_book.id} was successfully created.")
        print(f'\nКнига "{title}" добавлена в библиотеку!')

    def read(self) -> None:
        """Display all books in the library."""
        books_result: tuple[dict, list] | None = self._get_books()
        if not books_result:
            return

        print("\nВот что сейчас хранится в Библиотеке:")
        for book in books_result[1]:
            print(Book(**book))

        logger.info("Storage was successfully read.")

    def update(self) -> None:
        """Update the status of a book in the library."""
        books_result: tuple[dict, list] | None = self._get_books()
        if not books_result:
            return

        book_data, books = books_result

        book_id: str = input("Введите ID книги для смены статуса: ")
        for book in books:
            if book["id"] == book_id:
                print(f"\nТекущий статус книги: {book["status"]}")
                print("Доступные статусы:\n1. в наличии\n2. выдана")
                command: str = input("Введите новый статус книги: ")

                while command not in ["1", "2"]:
                    print("\nСтатус не определен!")
                    command = input("1. в наличии\n2. выдана\n")

                if command == "1":
                    book["status"] = BookStatus.AVAILABLE
                else:
                    book["status"] = BookStatus.BORROWED

                book_data["books"] = books
                self._write_storage(book_data)
                print(f"\nКнига {book_id} теперь {book["status"].value}!")
                logger.info(f"Book {book_id} was successfully updated.")
                break
        else:
            print(f"\nКнига {book_id} не найдена в Библиотеке!")
            logger.warning(f"Book {book_id} not found while try update.")

    def delete(self) -> None:
        """Remove a book from the library."""
        books_result: tuple[dict, list] | None = self._get_books()
        if not books_result:
            return

        book_data, books = books_result

        book_id: str = input("Введите ID книги для ее удаления: ")
        for book in books:
            if book["id"] == book_id:
                book_data["books"].remove(book)
                self._write_storage(book_data)
                print(f"\nКнига {book_id} удалена из Библиотеки!")
                logger.info(f"Book {book_id} was successfully deleted.")
                break
        else:
            print(f"\nКнига {book_id} не найдена в Библиотеке!")
            logger.warning(f"Book {book_id} not found while try delete.")

    def search_book(self):
        """Search for a book in the library."""
        books_result: tuple[dict, list] | None = self._get_books()
        if not books_result:
            return

        _, books = books_result

        print("Выберите парметр книги для поиска:")
        command: str = input("\n1. Название\n2. Автор\n3. Год выпуска\n")

        while command not in ["1", "2", "3"]:
            logger.warning("Command is not found while search book.")
            print("\nПараметр не определен!")
            command = input("\n1. Название\n2. Автор\n3. Год выпуска\n")

        find: str = input("\nВведите значение для поиска: ")
        parameter: str = "title"

        if command == "2":
            parameter = "author"
        elif command == "3":
            while not find.isdigit():
                print("\nГод выпуска должен быть числом!")
                find = input("\nВведите корректное значение года: ")

            parameter = "year"

        results: list = []
        for book in books:
            if str(book[parameter]).lower() == find.lower():
                results.append(book)

        if results:
            print(f"\nНайдено {len(results)} книг(и):")
            for book in results:
                print(Book(**book))
            logger.info(f"The search is complete. {len(results)} books found.")
        else:
            print("\nТакие книги не найдены!")
            logger.info("Result search is empty.")
