import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_flipkart(search="laptops", pages=1):
    """
    Uses Selenium to scrape Flipkart for laptop listings.
    :param pages: Number of pages to scrape
    :return: pandas.DataFrame containing product data
    """

    # Flipkart search URL for laptops
    base_url = f"https://www.flipkart.com/search?q={search}"

    # Initialize WebDriver (Chrome example)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment to run headless
    driver = webdriver.Chrome(options=options)

    # This list will hold all scraped product info
    all_products = []

    for page_num in range(1, pages + 1):
        url = f"{base_url}&page={page_num}"
        driver.get(url)

        # Wait a few seconds for page (and dynamic elements) to load
        time.sleep(3)

        # 1) Find all product containers by their parent class
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div.tUxRFH")
        print(f"Found {len(product_cards)} products on page {page_num}.")

        for card in product_cards:
            product_data = {}

            # -- Link --
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, "a.CGtC98")
                product_url = link_elem.get_attribute("href")
                product_data["product_url"] = product_url
            except:
                continue  # If no link, skip this product

            # -- Title --
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "div.KzDlHZ")
                product_data["title"] = title_elem.text.strip()
            except:
                product_data["title"] = None

            # -- Price --
            try:
                price_elem = card.find_element(By.CSS_SELECTOR, "div.Nx9bqj._4b5DiR")
                product_data["price"] = price_elem.text.strip()  # e.g. "₹31,990"
            except:
                product_data["price"] = None

            # -- MRP (Strikethrough Price) --
            try:
                mrp_elem = card.find_element(By.CSS_SELECTOR, "div.yRaY8j.ZYYwLA")
                product_data["mrp"] = mrp_elem.text.strip()  # e.g. "₹58,890"
            except:
                product_data["mrp"] = None

            # -- Discount --
            try:
                discount_elem = card.find_element(By.CSS_SELECTOR, "div.UkUFwK span")
                product_data["discount"] = discount_elem.text.strip()  # e.g. "45% off"
            except:
                product_data["discount"] = None

            # -- Rating --
            try:
                rating_elem = card.find_element(By.CSS_SELECTOR, "div.XQDdHH")
                product_data["rating"] = rating_elem.text.strip()  # e.g. "4.3"
            except:
                product_data["rating"] = None

            # -- Ratings & Reviews --
            try:
                rr_elem = card.find_element(By.CSS_SELECTOR, "span.Wphh3N")
                product_data["ratings_reviews"] = rr_elem.text.strip()
                # e.g. "1,517 Ratings & 86 Reviews"
            except:
                product_data["ratings_reviews"] = None

            all_products.append(product_data)

    # Close the driver
    driver.quit()

    # Convert to DataFrame
    pd.DataFrame(all_products).to_csv(f"flipkart_{search}.csv", index=False)
    return all_products


if __name__ == "__main__":
    # Example usage: scrape the first 2 pages
    scrape_flipkart(search="32 inch Smart TV", pages=2)
