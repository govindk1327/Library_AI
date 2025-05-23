import requests
import os
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("70b5336f9e785c681d5ff58906e6416124f80f59faa834164d297dcd8db63036")
BASE_URL = "https://data4library.kr/api/libSrchItemList"

def fetch_book_availability(isbn13: str) -> list[str] | None:
    if not isbn13:
        return None

    cache_key = f"book_availability_{isbn13}"
    cached = cache.get(cache_key)
    if cached is not None:
        print("✅ Availability from cache.")
        return cached

    params = {
        "authKey": API_KEY,
        "isbn13": isbn13,
        "format": "json"
    }

    try:
        resp = requests.get(BASE_URL, params=params)
        if resp.status_code != 200:
            print(f"❌ 도서관 API Error: {resp.status_code}")
            return None

        data = resp.json()
        docs = data.get("response", {}).get("lib", [])
        libraries = [lib["lib"]["libName"] for lib in docs]

        
        cache.set(cache_key, libraries, timeout=60 * 60)
        return libraries

    except Exception as e:
        print("❌ Exception while checking availability:", e)
        return None
