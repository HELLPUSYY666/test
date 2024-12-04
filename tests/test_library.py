import unittest
from library import Library, Book
import logging

logging.basicConfig(level=logging.INFO)


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library(storage_file="test_books.json")
        self.library.books = []

    def test_add_book(self):
        self.library.add_book("Title1", "Author1", 2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Title1")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_remove_book(self):
        self.library.add_book("Title1", "Author1", 2024)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        self.library.add_book("Title1", "Author1", 2024)
        results = self.library.search_books("Title1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Title1")

        results_empty = self.library.search_books("NonExistent")
        self.assertEqual(len(results_empty), 0)

    def test_update_status(self):
        self.library.add_book("Title1", "Author1", 2024)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")


if __name__ == "__main__":
    unittest.main()
