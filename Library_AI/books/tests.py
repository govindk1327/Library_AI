from django.test import TestCase
from books.models import Book, BookSource
from unittest.mock import patch
from books.library_api import fetch_book_availability

class BookModelTest(TestCase):
    def test_create_book_and_source(self):
        book = Book.objects.create(
            title="테스트 책",
            author="홍길동",
            publisher="테스트 출판사",
            pub_date="2024-05-15"
        )
        BookSource.objects.create(
            book=book,
            source="yes24",
            bestseller_rank=1,
            detail_url="https://yes24.com/test"
        )

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(book.sources.count(), 1)
    
    @patch("books.library_api.requests.get")
    def test_fetch_availability_success(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "response": {
                "lib": [
                    {"lib": {"libName": "강남도서관"}},
                    {"lib": {"libName": "서초도서관"}}
                ]
            }
        }

        isbn = "9791161571185"
        result = fetch_book_availability(isbn)
        self.assertIn("강남도서관", result)
        self.assertIn("서초도서관", result)

    @patch("books.library_api.requests.get")
    def test_fetch_availability_error(self, mock_get):
        mock_get.return_value.status_code = 500
        result = fetch_book_availability("1234567890123")
        self.assertIsNone(result)
