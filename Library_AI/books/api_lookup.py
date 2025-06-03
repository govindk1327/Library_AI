import requests

API_KEY = "70b5336f9e785c681d5ff58906e6416124f80f59faa834164d297dcd8db63036"

def search_book_external(title):
    url = f"https://data4library.kr/api/srchBooks?authKey={API_KEY}&title={title}&format=json"
    try:
        res = requests.get(url)
        data = res.json().get("response", {}).get("detail", [])
        if not data:
            return None
        doc = data[0]
        return {
            "title": doc["bookname"],
            "author": doc["authors"],
            "publisher": doc["publisher"],
            "pub_date": doc["publication_year"],
            "isbn13": doc["isbn13"]
        }
    except Exception as e:
        print("❌ External API error:", e)
        return None
