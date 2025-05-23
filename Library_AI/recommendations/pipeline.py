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


def extract_title(text: str) -> str:
    match = re.search(r"\[추천도서:\s*(.+?)\]", text)
    if match:
        return match.group(1).strip()
    numbered = re.search(r"\d+[.)]?\s*\*?\*?([^\n\*]+)", text)
    if numbered:
        return numbered.group(1).strip()
    return text.split("\n")[0][:40]

def apply_genre_filter(books_queryset, genres):
    # naive filter based on title/genre keywords
    return books_queryset.filter(
        title__icontains=genres[0]  # or more robust matching
    )

async def run_recommendation_pipeline(user_query: str, user=None) -> dict:
    print("🟢 Starting recommendation pipeline")
    
    print("▶️ Calling query_clova")
    clova_response = get_clova_response(user_query)
    print("✅ query_clova returned:", type(clova_response))

    answer = clova_response["answer"]
    prompt = clova_response["prompt"]
    print("📄 Clova answer:", answer[:60])

    title = extract_title(answer)
    print("🔍 Extracted title:", title)

    print("▶️ Looking up book in DB")

    books_qs = Book.objects.filter(title__icontains=title)

    # 🔁 Apply genre preference if user is authenticated
    if user:
        try:
            prefs = await sync_to_async(lambda: user.preferences)()
            genres = prefs.preferred_genres
            if genres:
                genre_kw = genres[0]  # Simple filter for demo; enhance as needed
                books_qs = books_qs.filter(title__icontains=genre_kw)
                print(f"🎯 Applied genre preference filter: {genre_kw}")
        except Exception as e:
            print("⚠️ Could not apply user preferences:", str(e))

    book = await sync_to_async(lambda: books_qs.first())()

    availability = []
    if book:
        if book.isbn13:
            availability = fetch_book_availability(book.isbn13)
        else:
            print("⚠️ Book found but missing ISBN13.")
    else:
        print("⚠️ No matching book in DB, skipping availability check.")

    print("✅ Book query done. Found:", bool(book))

    translator = Translator()
    translated = await translator.translate(answer, src="ko", dest="en")  
    print("✅ Translation result:", type(translated), translated.text[:60])
    translated_prompt = translated.text

    print("▶️ Generating image")
    image_path = generate_image(translated_prompt)
    print("✅ Image generated at:", image_path)

    print("▶️ Logging to PromptLog")
    if user:
        await sync_to_async(PromptLog.objects.create)(
            user=user,  # ✅ add this
            prompt_text=str(prompt),
            response_text=answer,
            user_query=user_query,
            book_isbns=book.id if book else "",
            created_at=timezone.now()
        )
    else:
        print("⚠️ Skipping prompt logging: no user provided.")

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