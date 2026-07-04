"""Main file for running the chatbot"""

from scrapper import get_articles
from converter import convert_article_to_markdown, save_markdown_to_file
from chatbot import create_chatbot
from utils import get_client
from utils import get_articles_api


def convert_save_articles_to_markdown(articles):
    for article in articles:
        markdown_content, file_name = convert_article_to_markdown(article)
        save_markdown_to_file(markdown_content, file_name)

if __name__ == "__main__":

    # TASK 1: Scrape articles from OptiSigns support center
    NUM_ARTICLES = 100   # at least 30
    limited_articles_link = f"{get_articles_api()}?page[size]={NUM_ARTICLES}"
    articles = get_articles(limited_articles_link, NUM_ARTICLES)
    
    if articles:
        convert_save_articles_to_markdown(articles)
        
    # TASK 2: Build RAG chatbot using the scraped articles
    client = get_client()
    # create a chatbot with a new file search store named "OptiSigns Search Store" and upload the scraped articles to it
    create_chatbot(client, "OptiSigns Search Store")
    
    # TASK 3: Daily jobs
    
    
    
    