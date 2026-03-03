# スクレイピング処理
import requests, logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
FIRST_PAGE = 1

def scrape_books():
    books = []
    page = FIRST_PAGE    
    
    while True:
        try:
            url = BASE_URL.format(page)
            logger.info(f"スクレイピングページ: {url}")
            
            res = requests.get(url, timeout=10)
            res.encoding = "utf-8" 
            if res.status_code == 404:
                logger.info("ページが存在しないため終了")
                break
            res.raise_for_status()
            
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.select("article.product_pod")
            
            if not items:
                logger.info("ページが存在しないため終了")
                break
            
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
                
            page += 1

        except requests.exceptions.Timeout:
            logger.error(f"ページ{page} タイムアウト")
            page += 1
            continue
        
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTPエラー: {e}")
            break
        
        except Exception as e:
            logger.error(f"予期せぬエラー: {e}")
            break
        
    logger.info(f"全ページスクレイピング完了 件数: {len(books)}")
    return books