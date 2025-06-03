import requests

API_KEY =  "70b5336f9e785c681d5ff58906e6416124f80f59faa834164d297dcd8db63036"

def fetch_cover_image(isbn13):
    if not isbn13:
        return None

    try:
        url = f"https://data4library.kr/api/srchDtlList"
        params = {
            "authKey": API_KEY,
            "isbn13": isbn13,
            "format": "json",
            "loaninfoYN": "Y",
            "displayInfo": "age"
        }

        resp = requests.get(url, params=params)
        if resp.status_code != 200 or not resp.text.strip():
            return None

        data = resp.json()
        doc = data.get("response", {}).get("detail", [{}])[0].get("book", {})
        return doc.get("bookImageURL")
    except Exception as e:
        print(f"❌ Failed to fetch cover image for ISBN {isbn13}: {e}")
        return None

