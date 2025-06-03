import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from books.models import Book, BookSource
from books.cover_fetcher import fetch_cover_image
import time
from datetime import datetime, timedelta

API_KEY = "70b5336f9e785c681d5ff58906e6416124f80f59faa834164d297dcd8db63036"
BASE_URL = "https://data4library.kr/api"

class Command(BaseCommand):
    help = "Fetch library popular and new arrival books"

    def add_arguments(self, parser):
        parser.add_argument('--libcode', type=str, help='Library code for new arrivals', default='148042')  # example
        parser.add_argument('--fetch', type=str, choices=['popular', 'new', 'both'], default='both')
        parser.add_argument('--start', type=str, help='Start date (yyyymmdd)', default='2025-05-01')
        parser.add_argument('--end', type=str, help='End date (yyyymmdd)', default='2025-05-25')

    def handle(self, *args, **options):
        today = datetime.today()

        # Auto-calculate default date ranges (correct format with hyphens)
        default_start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        default_end = today.strftime("%Y-%m-%d")
        default_month = today.strftime("%Y-%m")

        # Use CLI values if provided, else use the auto-calculated defaults
        start = options['start'] or default_start
        end = options['end'] or default_end
        lib_code = options['libcode']
        fetch_type = options['fetch']

        all_books = []

        # ✅ Log which date range is being used
        if fetch_type in ['popular', 'both']:
            print(f"📚 Fetching popular books from {start} to {end}")
            all_books += self.fetch_popular_books(startDt=start, endDt=end)

        if fetch_type in ['new', 'both']:
            print(f"📦 Fetching new arrival books for month: {default_month}")
            all_books += self.fetch_new_arrivals(lib_code, searchDt=default_month)
            
        count = 0
        for book_data in all_books:
            cover_url = book_data.get("image_url") or fetch_cover_image(book_data.get("isbn13"))

            book_obj, created = Book.objects.get_or_create(
                title=book_data["title"],
                author=book_data["author"],
                defaults={
                    "publisher": book_data["publisher"],
                    "pub_date": self.parse_date(book_data["pub_date"]),
                    "cover_image_url": cover_url
                }
            )

            # If already existed but missing cover image
            if not book_obj.cover_image_url and cover_url:
                book_obj.cover_image_url = cover_url
                book_obj.save()

            

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

    def fetch_popular_books(self, page=1, startDt="2025-05-01", endDt="2025-04-25"):
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

            # print(f"🔍 Requesting {url} with params: {params}")
            resp = requests.get(url, params=params)
            if resp.status_code == 504:
                print("⚠️ Timeout (504). Retrying once after 2s...")
                time.sleep(2)
                resp = requests.get(url, params=params)
                if resp.status_code == 504:
                    print("❌ Still failing. Skipping this page.")
                    break
            elif resp.status_code != 200:
                print(f"❌ API error (popular): {resp.status_code}")
                break
            elif not resp.text.strip():
                print("🛑 Empty response — likely end of pages.")
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
        
        print(f"✅ Fetched {len(books)} popular books between {startDt} and {endDt}")
        

        return books

    def fetch_new_arrivals(self, lib_code , searchDt="2025-05", page=1):
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

            # print(f"🔍 Requesting {url} with params: {params}")
            resp = requests.get(url, params=params)
            if resp.status_code != 200:
                print(f"❌ API error (new arrivals): {resp.status_code}")
                break

            if not resp.text.strip():
                print("🛑 Empty response — likely end of pages.")
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
                    "image_url": doc.get("bookImageURL", ""),  
                    "fetched_at": datetime.now().date()
                })


            page += 1
        print(f"✅ Fetched {len(books)} new arrival books for {lib_code}")

        return books
