from django.core.management.base import BaseCommand
from books.models import Book, BookSource
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

class Command(BaseCommand):
    help = "Fetch Yes24 bestseller books and insert into the database"

    def handle(self, *args, **options):
        books = self.fetch_yes24_bestsellers()
        for entry in books:
            book_obj, created = Book.objects.get_or_create(
                title=entry["title"],
                author=entry["author"],
                defaults={
                    "publisher": entry["publisher"],
                    "pub_date": self.parse_date(entry["pub_date"])
                }
            )

            BookSource.objects.update_or_create(
                book=book_obj,
                source="yes24",
                defaults={
                    "bestseller_rank": entry["rank"],
                    "detail_url": entry["book_url"]
                }
            )

        self.stdout.write(self.style.SUCCESS(f"Fetched and stored {len(books)} books from Yes24."))

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%y.%m.%d").date()
        except:
            return None

    def fetch_yes24_bestsellers(self):
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
        service = EdgeService()

        driver = webdriver.Edge(service=service, options=edge_options)
        driver.get("https://www.yes24.com/product/category/bestseller?categoryNumber=001")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-goods-no]"))
            )
        except:
            print("Timed out waiting for yes24 content to load.")
            driver.quit()
            return []

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        books = []
        for item in soup.select("li[data-goods-no]"):
            title_tag = item.select_one(".gd_name")
            subtitle_tag = item.select_one(".gd_nameE")
            author_tag = item.select_one(".info_auth a")
            publisher_tag = item.select_one(".info_pub a")
            pub_date_tag = item.select_one(".info_date")
            sale_price_tag = item.select_one(".info_price .txt_num em.yes_b")
            ori_price_tag = item.select_one(".info_price .dash em.yes_m")
            rating_tag = item.select_one(".rating_grade em.yes_b")
            review_tag = item.select_one(".rating_rvCount em.txC_blue")
            tag_list = [tag.get_text(strip=True) for tag in item.select(".info_tag .tag a")]
            image_tag = item.select_one(".lnk_img img")
            rank_tag = item.select_one("em.num")
            book_url = "https://www.yes24.com" + title_tag.get("href") if title_tag else ""
            image_url = image_tag.get("data-original") if image_tag else ""

            if title_tag and author_tag and publisher_tag and rank_tag:
                books.append({
                    "rank": int(rank_tag.get_text(strip=True)),
                    "title": title_tag.get_text(strip=True),
                    "subtitle": subtitle_tag.get_text(strip=True) if subtitle_tag else "",
                    "author": author_tag.get_text(strip=True),
                    "publisher": publisher_tag.get_text(strip=True),
                    "pub_date": pub_date_tag.get_text(strip=True) if pub_date_tag else "",
                    "price_sale": sale_price_tag.get_text(strip=True) if sale_price_tag else "",
                    "price_original": ori_price_tag.get_text(strip=True) if ori_price_tag else "",
                    "rating": rating_tag.get_text(strip=True) if rating_tag else "",
                    "reviews": review_tag.get_text(strip=True) if review_tag else "",
                    "tags": tag_list,
                    "image_url": image_url,
                    "book_url": book_url,
                    "source": "yes24"
                })

        return books
