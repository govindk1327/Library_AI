from django.test import TestCase
from rest_framework.test import APIClient
from books.models import Book

class APIIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="해리 포터",
            author="J.K. 롤링",
            publisher="문학수첩",
            pub_date="2000-01-01"
        )

    def test_get_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["results"]), 0)

    def test_search_books(self):
        response = self.client.get("/api/books/?q=해리")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("해리" in b["title"] for b in response.json()["results"]))

    def test_post_recommend_missing_query(self):
        response = self.client.post("/api/recommend/", {})
        self.assertEqual(response.status_code, 400)
