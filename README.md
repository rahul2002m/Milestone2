A simple Python project for **scraping and aggregating** competitor data (pricing, discounts, promotions) from Indian e-commerce websites (e.g., Amazon, Flipkart). The results are combined into a single dataset for further analysis or monitoring.

## Folder Structure

```
real_time_competitor_tracker/
│
├── scrapers/
│   ├── amazon_scraper.py        # Scraper for Amazon
│   ├── flipkart_scraper.py      # Scraper for Flipkart
│   └── __init__.py
│
├── aggregator/
│   ├── data_aggregator.py       # Combines data from scrapers
│   └── __init__.py
│
├── main.py                      # Example entry point for running the aggregation
├── requirements.txt             # Project dependencies
└── README.md                    # This README
```

### What Each Part Does

- **`scrapers/`**: Contains the scrapers for individual platforms.
  - **`amazon_scraper.py`**: Fetches product info (title, price, discount) from Amazon.
  - **`flipkart_scraper.py`**: Fetches product info from Flipkart.
- **`aggregator/`**: Holds logic to merge scraped data into a unified format.
  - **`data_aggregator.py`**: Calls each scraper and saves the combined results as JSON.
- **`main.py`**: Shows how to run the scrapers and aggregator.

## How to Run

1. **Clone this repository** (or download the files):
   ```bash
   git clone https://github.com/your-username/real_time_competitor_tracker.git
   cd real_time_competitor_tracker
   ```

2. **Install dependencies** (ideally in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. **Edit `main.py`** to include the product names you want to scrape. For example:
   ```python
   product_map = {
       "amazon": [
           "iWatch series 10",
           "samsung 32 inch tv"
           # Add more Amazon product URLs here
       ],
       "flipkart": [
           "iWatch series 10",
           "samsung 32 inch tv"
           # Add more Flipkart product URLs here
       ]
   }
   ```

4. **Run the script**:
   ```bash
   python main.py
   ```
   - This will scrape each product URL and create a file named `aggregated_data.json` with the results.

5. **Check Output**:  
   Open `aggregated_data.json` to see the data in JSON format.

That’s it! You now have a simple scraper setup to monitor competitor strategies on Indian e-commerce sites. Adjust the code as needed for additional platforms or to customize the data fields you collect.
