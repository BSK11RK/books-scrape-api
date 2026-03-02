# スクレイピング処理
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

def scrape_books():
    res = requests.get(BASE_URL)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    books = []
    
    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"]
        price = book.select_one("p.price_color").text
        availability = book.select_one("p.instock.availability").text.strip()
        books.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    return books