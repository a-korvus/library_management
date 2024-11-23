"""Some tests in the app."""

import os
import shutil
import unittest

from config import BASE_DIR, preparation
from handler import Library


class TestLibrary(unittest.TestCase):
    """Test cases for the Library class."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.test_data: dict = {
            "books": [
                {
                    "id": "19f3bcc1-a02a-4cc4-a8b8-f92809ffdcea",
                    "title": "Гибель богов",
                    "author": "Ник Перумов",
                    "year": 1994,
                    "status": "в наличии",
                },
                {
                    "id": "c78b9870-0a6a-4f70-b22f-a907057dcee8",
                    "title": "Братство Кольца",
                    "author": "Джон Толкин",
                    "year": 1954,
                    "status": "выдана",
                },
                {
                    "id": "a14caaf5-4f83-4581-bb86-37e592002098",
                    "title": "Последнее желание",
                    "author": "Анджей Сапковский",
                    "year": 1993,
                    "status": "выдана",
                },
                {
                    "id": "52bb0d13-9537-4e40-bf0a-3f2e89f337a5",
                    "title": "Первое правило волшебника",
                    "author": "Терри Гудкайнд",
                    "year": 1994,
                    "status": "в наличии",
                },
            ]
        }

        self.test_dir_path: str = os.path.join(BASE_DIR, "test_storage")
        self.test_file_path: str = os.path.join(
            self.test_dir_path,
            "test_storage.json",
        )
        self.library: Library = Library(storage_path=self.test_file_path)

        preparation(
            dirs_exists=[self.test_dir_path],
            files_exists=[self.test_file_path],
        )

    def test_write_read_storage(self):
        """Testing writting to file and readung file."""
        self.library._write_storage(self.test_data)
        self.assertEqual(self.library._read_storage(), self.test_data)

    def test_get_books_empty(self):
        """Testing getting books from empty file."""
        self.assertEqual(self.library._get_books(), None)

    def test_get_books(self):
        """Testing getting books from file."""
        self.library._write_storage(self.test_data)
        self.assertEqual(
            self.library._get_books(),
            (self.test_data, self.test_data["books"])
        )

    def test_read_empty_storage(self):
        """Testing reading from empty file."""
        self.assertEqual(self.library.read(), None)

    def tearDown(self):
        """Clean after all tests."""
        if os.path.exists(self.test_dir_path):
            shutil.rmtree(self.test_dir_path)


if __name__ == "__main__":
    unittest.main()
