"""Scrapper for OptiSigns support articles."""

import requests
from utils import get_articles_api_url


def get_articles(api, NUM_ARTICLES=None):
    response = requests.get(api)

    if response.status_code != 200:
        print("Failed to retrieve articles!")
    else:
        log_string = f"Successfully retrieved {NUM_ARTICLES} articles." if NUM_ARTICLES else "Successfully retrieved articles."
        print(log_string)
        data = response.json()
        
        # Print the content of the first article for debugging
        # first_article_updated_at = data["articles"][0]["updated_at"]
        # print("First article updated at:", first_article_updated_at)
        
        return data["articles"]
    
if __name__ == "__main__":
    # Test the scrapper by fetching 100 articles
    get_articles(get_articles_api_url(), 100)
