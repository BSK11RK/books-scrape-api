from apscheduler.schedulers.background import BackgroundScheduler
from backend.scraper import scrape_books
from backend.exporter import save_all_formats
from backend.graph import generate_graph

scheduler = BackgroundScheduler()

def job():
    books = scrape_books()
    save_all_formats(books)
    generate_graph()
    
def start():
    scheduler.add_job(job, "interval", minutes=10)
    scheduler.start()