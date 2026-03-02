from apscheduler.schedulers.background import BackgroundScheduler
from backend.scraper import scrape_books
from backend.exporter import save_all_formats
from backend.graph import generate_graph
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def job():
    logger.info("定期スクレイピング実行開始")
    
    books = scrape_books()
    save_all_formats(books)
    generate_graph()
    
    logger.info("定期スクレイピング実行完了")
    
def start():
    scheduler.add_job(job, "interval", minutes=10)
    scheduler.start()
    logger.info("スケジューラ起動完了")