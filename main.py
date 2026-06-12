import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

# Logging Configuration
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "https://quotes.toscrape.com/"


def scrape_quotes():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        quotes = []

        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text

            quotes.append({
                "Quote": text,
                "Author": author,
                "Scraped_Time": datetime.now()
            })

        return quotes

    except requests.exceptions.RequestException as e:
        logging.error(f"Error Occurred: {e}")
        return []


def save_to_csv(data):
    if data:
        df = pd.DataFrame(data)
        df.to_csv("quotes.csv", index=False)
        print("Data saved successfully!")
        logging.info("CSV file created successfully")
    else:
        print("No data found.")


if __name__ == "__main__":
    data = scrape_quotes()
    save_to_csv(data)