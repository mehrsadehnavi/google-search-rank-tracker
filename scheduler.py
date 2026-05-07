import schedule
import time
from scraper import search_keywords

def run_scheduler():
    schedule.every().day.at("10:00").do(search_keywords)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    run_scheduler()
