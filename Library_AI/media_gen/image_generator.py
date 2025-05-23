import requests
import os
import hashlib
from django.core.cache import cache

STABILITY_API_KEY = "sk-zg027ArNEiNxC2SefdjgmUbpjBwCBR2uOmALJPgSrClvnJDW"
STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

def generate_image(prompt_text: str, save_dir: str = "generated_images") -> str | None:
   
    prompt_hash = hashlib.md5(prompt_text.encode()).hexdigest()
    filename = f"{prompt_hash}.png"
    image_path = os.path.join(save_dir, filename)

    os.makedirs(save_dir, exist_ok=True)

    cache_key = f"stability_image_{prompt_hash}"
    cached = cache.get(cache_key)
    if cached and os.path.exists(cached):
        print("🧠 Image found in Redis cache.")
        return cached

    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_API_KEY}",
    }

    files = {
        "prompt": (None, prompt_text),
        "mode": (None, "text-to-image"),
        "output_format": (None, "png"),
        "aspect_ratio": (None, "1:1"),
    }

    response = requests.post(STABILITY_URL, headers=headers, files=files)

    if response.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(response.content)
        cache.set(cache_key, image_path, timeout=60 * 60)  
        return image_path
    else:
        print("❌ Stability AI error:", response.status_code, response.text)
        return None