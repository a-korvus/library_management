"""The entrypoint to the small console python app."""

from config import (
    COMMANDS,
    STORAGE_BOOKS,
    STORAGE_DIR,
    preparation,
    show_commands,
)
from handler import Library


def main() -> None:
    """The main app function."""
    preparation(dirs_exists=[STORAGE_DIR], files_exists=[STORAGE_BOOKS])
    library: Library = Library(storage_path=STORAGE_BOOKS)

    print("Добро пожаловать в Библиотеку Ватикана!", end="\n\n")
    show_commands(commands=COMMANDS)

    command: str = input("Для продолжения введите номер команды: ")
    while command not in COMMANDS.keys():
        if command == "exit":
            print("\nДо свидания!")
            break
        print("\nКоманда не найдена! Для выхода из программы введите 'exit'")
        command = input("Для продолжения введите номер команды: ")

    if command == "1":
        library.create()
    elif command == "2":
        library.delete()
    elif command == "3":
        library.search_book()
    elif command == "4":
        library.read()
    elif command == "5":
        library.update()


if __name__ == "__main__":
    main()
