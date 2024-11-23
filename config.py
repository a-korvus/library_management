"""Main projects settings."""

import json
import os

from config_log import get_logger

logger = get_logger(__name__)

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
COMMANDS: dict[str, str] = {
    "1": "Добавление книги",
    "2": "Удаление книги",
    "3": "Поиск книги",
    "4": "Отображение всех книг",
    "5": "Изменение статуса книги",
}

STORAGE_DIR: str = os.path.join(BASE_DIR, "storage")
STORAGE_BOOKS: str = os.path.join(STORAGE_DIR, "books.json")


def preparation(dirs_exists: list[str], files_exists: list[str]) -> None:
    """Preparation of the app."""
    for dir_path in dirs_exists:
        if not os.path.exists(dir_path):
            """Check if dir exists, create it or not."""
            os.makedirs(dir_path)
            logger.info(f"Directory {dir_path} created.")
        else:
            logger.info(f"Directory {dir_path} already exists.")

    for file_path in files_exists:
        if not os.path.exists(file_path):
            """Check if file exists, create it or not."""
            with open(file_path, "w", encoding="utf-8") as file:
                dummy: dict = {"books": []}
                json.dump(dummy, file, ensure_ascii=False, indent=4)
            logger.info(f"File {file_path} created.")
        else:
            logger.info(f"File {file_path} already exists.")

    logger.info("Preparation completed.")


def show_commands(commands: dict):
    """Show all commands to user."""
    print("Доступные команды:")
    for num, com in commands.items():
        print(f"{num}: {com}")
