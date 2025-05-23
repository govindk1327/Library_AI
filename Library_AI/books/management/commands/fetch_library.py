import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from books.models import Book, BookSource

API_KEY = "70b5336f9e785c681d5ff58906e6416124f80f59faa834164d297dcd8db63036"
BASE_URL = "https://data4library.kr/api"

class Command(BaseCommand):
    help = "Fetch library popular and new arrival books"

    def add_arguments(self, parser):
        parser.add_argument('--libcode', type=str, help='Library code for new arrivals', default='148042')  # example
        parser.add_argument('--fetch', type=str, choices=['popular', 'new', 'both'], default='both')
        parser.add_argument('--start', type=str, help='Start date (yyyymmdd)', default='2025-04-01')
        parser.add_argument('--end', type=str, help='End date (yyyymmdd)', default='2025-04-30')

    def handle(self, *args, **options):
        lib_code = options['libcode']
        start = options['start']
        end = options['end']
        fetch_type = options['fetch']

        all_books = []

        if fetch_type in ['popular', 'both']:
            all_books += self.fetch_popular_books(startDt=start, endDt=end)

        if fetch_type in ['new', 'both']:
            all_books += self.fetch_new_arrivals(lib_code)

        count = 0
        for book_data in all_books:
            book_obj, created = Book.objects.get_or_create(
                title=book_data["title"],
                author=book_data["author"],
                defaults={
                    "publisher": book_data["publisher"],
                    "pub_date": self.parse_date(book_data["pub_date"])
                }
            )

            BookSource.objects.update_or_create(
                book=book_obj,
                source=book_data["source"],
                defaults={
                    "bestseller_rank": book_data.get("rank"),
                    "detail_url": book_data.get("detail_url", "")
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Fetched and stored {count} books from library API."))

    def parse_date(self, year_str):
        try:
            return datetime.strptime(year_str, "%Y").date()
        except:
            return None

    def safe_get_json(self, resp):
        try:
            return resp.json()
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
            print("❌ Response text was:", resp.text[:300])  
            return {}

    def fetch_popular_books(self, page=1, startDt="2025-04-01", endDt="2025-04-30"):
        books = []
        while True:
            url = f"{BASE_URL}/loanItemSrch"
            params = {
                "authKey": API_KEY,
                "startDt": startDt,
                "endDt": endDt,
                "pageNo": page,
                "pageSize": 50,
                "format": "json"
            }

            print(f"🔍 Requesting {url} with params: {params}")
            resp = requests.get(url, params=params)
            if resp.status_code != 200:
                print(f"❌ API error (popular): {resp.status_code}")
                break

            docs = self.safe_get_json(resp).get("response", {}).get("docs", [])
            if not docs:
                break

            for idx, item in enumerate(docs):
                doc = item.get("doc", {})
                books.append({
                    "title": doc.get("bookname", "").strip(),
                    "author": doc.get("authors", "").strip(),
                    "publisher": doc.get("publisher", "").strip(),
                    "pub_date": doc.get("publication_year", ""),
                    "isbn13": doc.get("isbn13", ""),
                    "source": "library",
                    "rank": idx + 1 + (page - 1) * 50,
                    "detail_url": "",
                    "fetched_at": datetime.now().date()
                })

            page += 1

        return books

    def fetch_new_arrivals(self, lib_code , searchDt="2025-04", page=1):
        books = []
        while True:
            url = f"{BASE_URL}/newArrivalBook"
            params = {
                "authKey": API_KEY,
                "libCode": lib_code,
                "pageNo": page,
                "pageSize": 1,
                "format": "json"
            }
            if searchDt:
                params["searchDt"] = searchDt

            print(f"🔍 Requesting {url} with params: {params}")
            resp = requests.get(url, params=params)
            if resp.status_code != 200:
                print(f"❌ API error (new arrivals): {resp.status_code}")
                break

            docs = self.safe_get_json(resp).get("response", {}).get("docs", [])
            if not docs:
                break

            for item in docs:
                doc = item.get("doc", {})
                books.append({
                    "title": doc.get("bookname", "").strip(),
                    "author": doc.get("authors", "").strip(),
                    "publisher": doc.get("publisher", "").strip(),
                    "pub_date": doc.get("publication_year", ""),
                    "isbn13": doc.get("isbn13", ""),
                    "source": "library_new",
                    "rank": None,
                    "detail_url": "",
                    "fetched_at": datetime.now().date()
                })

            page += 1

        return books
