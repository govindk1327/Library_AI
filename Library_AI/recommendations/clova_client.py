import requests
import re
from django.core.cache import cache

CLOVA_API_KEY = "nv-270db94eb8bf42108110b22f551e655axCwf"
CLOVA_API_URL = "https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-003"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CLOVA_API_KEY}"
}

def get_clova_response(user_query: str) -> dict:
    prompt = {
        "messages": [
            {
                "role": "system",
                "content": "당신은 사용자에게 책을 추천하는 AI입니다. 제목은 반드시 다음 형식으로 출력하세요: [추천도서: <제목>]. 이유도 함께 설명해주세요."
            },
            {"role": "user", "content": user_query}
        ],
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9
    }

   

    cache_key = f"clova_response_{hash(user_query)}"
    cached = cache.get(cache_key)
    if cached:
        return {"answer": cached, "prompt": prompt}

    response = requests.post(CLOVA_API_URL, headers=HEADERS, json=prompt)
    response.raise_for_status()
    answer = response.json().get("result", {}).get("message", {}).get("content", "").strip()

    cache.set(cache_key, answer, timeout=60 * 60)  

    return {"answer": answer, "prompt": prompt}
