# スクレイピング処理
import requests, logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/"

def scrape_books():
    try:
        logger.info("スクレイピング開始")
        
        res = requests.get(BASE_URL)
        res.encoding = "utf-8" 
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, "html.parser")
        books = []
        
        for book in soup.select("article.product_pod"):
            title = book.h3.a["title"]
            raw_price = book.select_one("p.price_color").text
            price = (
                raw_price.replace("£", "")
                .replace("Â", "")
                .strip()
            )
            price = float(price)
            availability = book.select_one("p.instock.availability").text.strip()
            books.append({
                "title": title,
                "price": price,
                "availability": availability
            })

        logger.info(f"スクレイピング成功 件数: {len(books)}")
        return books
    except Exception as e:
        logger.error(f"スクレイピング失敗: {e}")
        return []