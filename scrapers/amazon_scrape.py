import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_amazon(search="laptops", pages=1):
    """
    Uses Selenium to scrape Amazon.in for laptop listings.
    :param pages: Number of pages to scrape
    :return: pandas.DataFrame containing product data
    """

    # Base URL for searching "laptops" on Amazon.in
    base_url = f"https://www.amazon.in/s?k={search}"

    # Initialize Selenium WebDriver (Chrome example)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run headless (no browser window)
    driver = webdriver.Chrome(options=options)

    all_products = []

    for page_num in range(1, pages + 1):
        # Construct the page URL (Amazon paginates with `&page=`)
        url = f"{base_url}&page={page_num}"
        driver.get(url)

        # Wait a few seconds for the page to load fully
        time.sleep(3)

        # 1) Find all product containers
        #    Based on your snippet, we look for:
        #    <div class="puis-card-container s-card-container s-overflow-hidden ..."
        product_cards = driver.find_elements(
            By.CSS_SELECTOR, "div.puis-card-container.s-card-container"
        )
        print(f"Found {len(product_cards)} products on page {page_num}.")

        for card in product_cards:
            product_data = {}

            # -----------------------
            # Title + Link
            # -----------------------
            # a) Link element: <a class="a-link-normal s-line-clamp-2 s-link-style a-text-normal" ...>
            # b) Title text is in: <h2 class="a-size-medium ..."><span>...</span></h2>
            try:
                link_elem = card.find_element(
                    By.CSS_SELECTOR,
                    "a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal",
                )
                product_url = link_elem.get_attribute("href")
                product_data["product_url"] = product_url

                title_elem = card.find_element(
                    By.CSS_SELECTOR,
                    "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span",
                )
                product_data["title"] = title_elem.text.strip()
            except:
                # If we cannot get title/link, skip this card
                continue

            # -----------------------
            # Price
            # -----------------------
            # Inside:
            #   <div data-cy="price-recipe">
            #       <span class="a-price">
            #           <span class="a-offscreen">₹51,990</span>
            #       ...
            try:
                price_elem = card.find_element(
                    By.CSS_SELECTOR,
                    "div[data-cy='price-recipe'] span.a-price span.a-offscreen",
                )
                product_data["price"] = price_elem.text.strip()
            except:
                product_data["price"] = None

            # -----------------------
            # Rating
            # -----------------------
            # Inside:
            #   <div data-cy="reviews-block">
            #       <i class="a-icon a-icon-star-small ...">
            #           <span class="a-icon-alt">3.6 out of 5 stars</span>
            #       </i>
            try:
                rating_elem = card.find_element(
                    By.CSS_SELECTOR,
                    "div[data-cy='reviews-block'] i.a-icon-star-small span.a-icon-alt",
                )
                full_rating_text = rating_elem.get_attribute(
                    "innerHTML"
                ).strip()  # e.g. "3.6 out of 5 stars"
                # Extract numeric portion if desired
                if " out of 5 stars" in full_rating_text.lower():
                    product_data["rating"] = (
                        full_rating_text.lower().split(" out of")[0].strip()
                    )
                else:
                    product_data["rating"] = full_rating_text
            except:
                product_data["rating"] = None

            # -----------------------
            # Number of Ratings
            # -----------------------
            # Inside:
            #   <a class="a-link-normal s-underline-text s-underline-link-text s-link-style" ...>
            #       <span class="a-size-base s-underline-text">779</span>
            #   </a>
            try:
                ratings_count_elem = card.find_element(
                    By.CSS_SELECTOR,
                    "div[data-cy='reviews-block'] a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style span",
                )
                product_data["ratings_count"] = ratings_count_elem.text.strip()
            except:
                product_data["ratings_count"] = None

            # Append the collected data
            all_products.append(product_data)

    # Quit the driver after scraping
    driver.quit()

    # Convert results to a DataFrame
    pd.DataFrame(all_products).to_csv(f"amazon_{search}.csv", index=False)
    return all_products


if __name__ == "__main__":
    # Example usage: scrape the first 2 pages
    scrape_amazon(search="32 inch Smart TV", pages=2)
