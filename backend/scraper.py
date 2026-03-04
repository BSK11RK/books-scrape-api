# スクレイピング処理
import httpx, asyncio, logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

async def fetch_page(client: httpx.AsyncClient, page: int):
    url = BASE_URL.format(page)
    
    try:
        logger.info(f"[START] ページ取得開始: page={page}")
        
        res = await client.get(url)
        res.raise_for_status()
        
        logger.info(f"[SUCCESS] ページ取得成功: page={page}")
        
        return res.text
    
    except httpx.RequestError as e:
        logger.error(f"[ERROR] リクエスト失敗: page={page} error={e}")
        return None
    
    except httpx.HTTPStatusError as e:
        logger.error(f"[ERROR] HTTPエラー: page={page} status={e.response.status_code}")
        return None
    
async def scrape_books_async():
    books = []
    logger.info("=== 非同期スクレイピング開始 ===")
    
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_page(client, i) for i in range(1, 51)]
        pages = await asyncio.gather(*tasks)
        
        for idx, html in enumerate(pages, start=1):
            if html is None:
                logger.warning(f"[SKIP] page={idx} は取得失敗のためスキップ")
                continue
            
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select(".product_pod")
            logger.info(f"[PARSE] page={idx} 商品数={len(items)}")
            
            for item in items:
                try:
                    title = item.h3.a["title"]
                    raw_price = item.select_one(".price_color").text
                    price = float(raw_price.replace("£", "").strip())

                    availability = (
                        item.select_one(".availability")
                        .text.strip()
                    )

                    books.append({
                        "title": title,
                        "price": price,
                        "availability": availability,
                    })

                except Exception as e:
                    logger.error(f"[ERROR] 商品解析失敗: page={idx} error={e}")
                    
    logger.info(f"=== スクレイピング完了: 総取得件数={len(books)} ===")

    return books

def scrape_books():
    import asyncio
    return asyncio.run(scrape_books_async())