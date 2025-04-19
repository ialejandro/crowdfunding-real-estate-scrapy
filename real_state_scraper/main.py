#!/usr/bin/env python3
"""
Real Estate Crowdfunding Scraper

This script scrapes real estate crowdfunding projects from multiple platforms
and combines the results into a single CSV file.
"""

import csv
import os
import logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from real_state_scraper.spiders.urbanitae import UrbanitaeOpenProjectsSpider
from real_state_scraper.spiders.wecity import WecityOpenProjectsSpider

# Configuration
CSV_FILES = {
    "urbanitae": "urbanitae.csv",
    "wecity": "wecity.csv",
}
FINAL_CSV = "real_estate_crowdfunding.csv"
FIELD_ORDER = [
    "platform",
    "title",
    "city",
    "region",
    "address",
    "status",
    "total_return",
    "term_months",
    "business_model",
    "url"
]

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def remove_old_files():
    """
    Remove old CSV files before starting a new scrape.

    This ensures we don't have stale data from previous runs.
    """
    for file in list(CSV_FILES.values()) + [FINAL_CSV]:
        if os.path.exists(file):
            try:
                os.remove(file)
                logging.info(f"Removed old file: {file}")
            except OSError as e:
                logging.error(f"Error removing file {file}: {e}")

def write_csv(items, output_file):
    """
    Write items to a CSV file.

    Args:
        items: List of dictionaries containing the data
        output_file: Path to the output CSV file
    """
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_ORDER)
            writer.writeheader()
            writer.writerows(items)
        logging.info(f"Successfully wrote {len(items)} items to {output_file}")
    except IOError as e:
        logging.error(f"Error writing to {output_file}: {e}")

def load_csv(file_path):
    """
    Load data from a CSV file.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dictionaries containing the data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")
        return []

def deduplicate(items, key="url"):
    """
    Remove duplicate items based on a key.

    Args:
        items: List of dictionaries containing the data
        key: Key to use for deduplication

    Returns:
        List of dictionaries with duplicates removed
    """
    seen = {}
    for item in items:
        k = item.get(key)
        if k:
            seen[k] = item
    return list(seen.values())

@defer.inlineCallbacks
def crawl_all():
    """
    Run all spiders and combine their results.

    This function:
    1. Runs each spider in sequence
    2. Loads the results from each CSV file
    3. Deduplicates the combined results
    4. Writes the final CSV file
    """
    logger = setup_logging()
    logger.info("Starting scraping process")

    # Urbanitae spider
    logger.info("Running Urbanitae spider")
    runner = CrawlerRunner(settings={
        "FEEDS": {
            CSV_FILES["urbanitae"]: {"format": "csv", "overwrite": True},
        },
        "LOG_LEVEL": "WARNING"
    })
    yield runner.crawl(UrbanitaeOpenProjectsSpider)

    # Wecity spider
    logger.info("Running Wecity spider")
    runner = CrawlerRunner(settings={
        "FEEDS": {
            CSV_FILES["wecity"]: {"format": "csv", "overwrite": True},
        },
        "LOG_LEVEL": "WARNING"
    })
    yield runner.crawl(WecityOpenProjectsSpider)

    all_items = []
    for file in CSV_FILES.values():
        items = load_csv(file)
        all_items.extend(items)
        logger.info(f"Loaded {len(items)} items from {file}")

    # deduplicate and write final CSV
    deduped = deduplicate(all_items)
    write_csv(deduped, FINAL_CSV)

    logger.info(f"✅ Scraping complete. Combined CSV saved to: {FINAL_CSV}")
    reactor.stop()

if __name__ == "__main__":
    configure_logging()
    remove_old_files()
    crawl_all()
    reactor.run()
