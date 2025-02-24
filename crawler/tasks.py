from celery import shared_task
from .crawler import EsmerdisScraper
import logging

logger = logging.getLogger(__name__)

@shared_task
def run_scraper():
    logger.info("Starting scraper...")
    scraper = EsmerdisScraper()
    scraper.scrape_all_pages()
    logger.info("Scraper finished.")
