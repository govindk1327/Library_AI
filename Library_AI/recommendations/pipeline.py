import re
from googletrans import Translator
from django.utils import timezone
from recommendations.clova_client import get_clova_response
from media_gen.image_generator import generate_image
from books.models import Book
from recommendations.models import PromptLog
from media_gen.models import MediaAsset
from asgiref.sync import sync_to_async
from books.library_api import fetch_book_availability
from books.api_lookup import search_book_external  
from books.cover_fetcher import fetch_cover_image


import re

def extract_title(text: str) -> str:
    # Try [추천도서: <title>] OR [추천도서 : <title>] (with space)
    match = re.search(r"\[추천도서\s*[:：]\s*(.+?)\]", text)
    if match:
        return match.group(1).strip()

    # Fallback: first **bold** title
    numbered = re.search(r"\d+[.)]?\s*\*+\s*(.+?)\s*\*+", text)
    if numbered:
        return numbered.group(1).strip()

    # Final fallback: first non-empty line (max 40 chars)
    return next((line for line in text.splitlines() if line.strip()), text)[:40].strip()



async def run_recommendation_pipeline(user_query: str, user=None) -> dict:
    print("🟢 Starting recommendation pipeline")

    # 🔄 Language prompt setup
    lang = "ko"
    if user:
        try:
            prefs = await sync_to_async(lambda: user.preferences)()
            lang = prefs.preferred_language or "ko"
        except Exception as e:
            print("⚠️ Could not load user preferences:", e)

    prompt_text = {
        "ko": "당신은 사용자에게 책을 추천하는 AI입니다. 제목은 반드시 다음 형식으로 출력하세요: [추천도서: <제목>]. 이유도 함께 설명해주세요.",
        "en": "You are an AI that recommends books to users. Always format the title as: [Recommended: <title>]. Include an explanation too.",
    }[lang]

    print("▶️ Calling query_clova")
    clova_response = get_clova_response(user_query, system_prompt=prompt_text)
    print("✅ query_clova returned:", type(clova_response))

    answer = clova_response["answer"]
    prompt = clova_response["prompt"]
    print("📄 Clova answer:", answer[:60])

    title = extract_title(answer)
    print("🔍 Extracted title:", title)

    print("▶️ Looking up book in DB")
    books_qs = Book.objects.filter(title__icontains=title)

    if user and prefs and prefs.preferred_genres:
        genre_kw = prefs.preferred_genres[0]
        books_qs = books_qs.filter(title__icontains=genre_kw)
        print(f"🎯 Applied genre filter: {genre_kw}")

    book = await sync_to_async(lambda: books_qs.first())()

    # 🔁 Fallback to external API if not found
    if not book:
        print("🔍 Not found in DB, trying external API...")
        book_data = await sync_to_async(search_book_external)(title)
        if book_data:
            book = await sync_to_async(Book.objects.create)(
                title=book_data["title"],
                author=book_data["author"],
                publisher=book_data["publisher"],
                pub_date=book_data["pub_date"],
                isbn13=book_data["isbn13"]
            )
            print("✅ Book added to DB via API.")
        else:
            print("❌ Book not found via external API.")

    availability = []
    if book and book.isbn13:
        availability = fetch_book_availability(book.isbn13)

    # 🌍 Translate only if needed
    translated_prompt = answer
    if lang == "en":
        translator = Translator()
        translated = await translator.translate(answer, src="ko", dest="en")
        translated_prompt = translated.text
        print("✅ Translated Clova output to EN")

    image_path = None

    if prefs.prefers_ai_images:
        print("▶️ Generating AI image")
        image_path = generate_image(translated_prompt)
        print("✅ AI image generated at:", image_path)
    else:
        print("▶️ User prefers real cover image")
        if book:
            if not book.cover_image_url:
                print("🔍 Fetching real book cover...")
                cover_url = await sync_to_async(fetch_cover_image)(book.isbn13)
                if cover_url:
                    book.cover_image_url = cover_url
                    await sync_to_async(book.save)()
                else:
                    print("⚠️ No cover image found")
            image_path = book.cover_image_url or "NO_COVER"
        else:
            print("⚠️ No book to fetch cover image for")
            image_path = "NO_COVER"

    # print("▶️ Generating image")
    # image_path = generate_image(translated_prompt)
    # print("✅ Image generated at:", image_path)

    if user:
        print("▶️ Logging to PromptLog")
        await sync_to_async(PromptLog.objects.create)(
            user=user,
            prompt_text=str(prompt),
            response_text=answer,
            user_query=user_query,
            book_isbns=book.id if book else "",
            created_at=timezone.now()
        )
        print("✅ PromptLog saved")

    if book and image_path:
        print("▶️ Saving media asset")
        await sync_to_async(MediaAsset.objects.create)(
            book=book,
            media_type="image",
            media_url=image_path,
            summary=answer,
        )
        print("✅ MediaAsset saved")

    print("✅ Pipeline complete. Returning data.")
    return {
        "query": user_query,
        "ai_response": answer,
        "recommended_title": title,
        "book_metadata": {
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "isbn13": book.isbn13
        } if book else None,
        "availability": availability,
        "image_path": image_path,
        "note": "Book found in DB" if book else "Book not found"
    }
