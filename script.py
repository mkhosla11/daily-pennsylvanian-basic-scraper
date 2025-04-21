"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru
import time
from bs4 import BeautifulSoup
from loguru import logger


def scrape_data_point():
    """
    Scrapes the #1 most read article title from The Daily Pennsylvanian homepage.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    # Respect the crawl-delay of 10 seconds
    time.sleep(10)

    url = "https://www.thedp.com"
    try:
        response = requests.get(url, timeout=10)
        logger.info(f"Request URL: {response.url}")
        logger.info(f"Request status code: {response.status_code}")

        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            # Select the first link in the Most Read section
            most_read_section = soup.find("div", class_="most-read")
            if most_read_section:
                first_article = most_read_section.find("a")
                if first_article:
                    data_point = first_article.get_text(strip=True)
                    logger.info(f"Data point: {data_point}")
                    return data_point
            logger.warning("Most Read section or first article not found.")
        else:
            logger.error(f"Failed to fetch the page. Status code: {response.status_code}")
    except requests.RequestException as e:
        logger.error(f"An error occurred: {e}")

    return ""


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
