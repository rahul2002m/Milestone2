import json
import logging

from scrapers.amazon_scrape import scrape_amazon
from scrapers.flipkart_scrape import scrape_flipkart

logging.basicConfig(level=logging.INFO)


def collect_data(product_map):
    """
    Aggregates data from multiple e-commerce sites.
    """
    aggregated_data = {}

    # Amazon scraping
    if "amazon" in product_map:
        for item in product_map["amazon"]:
            amazon_data = scrape_amazon(item, 1)
            aggregated_data["amazon"] = amazon_data

    # Flipkart scraping
    if "flipkart" in product_map:
        for item in product_map["flipkart"]:
            amazon_data = scrape_flipkart(item, 1)
            aggregated_data["flipkart"] = amazon_data

    return aggregated_data


def save_to_json(data, filename="aggregated_data.json"):
    """
    Saves the aggregated data to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logging.info(f"Data saved to {filename}")


def run(product_map):
    """
    Orchestrates data scraping and returns final aggregated results.
    """
    data = collect_data(product_map)
    save_to_json(data)
    return data
