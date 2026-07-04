"""One-shot scraper and Gemini File Search sync job."""

from converter import convert_article_to_markdown, save_markdown_to_file
from daily_jobs import sync_articles_to_store
from scrapper import get_articles
from uploader import get_or_create_file_search_store
from utils import  get_articles_api_url, get_client


def convert_save_articles_to_markdown(articles):
    for article in articles:
        markdown_content, file_name = convert_article_to_markdown(article)
        save_markdown_to_file(markdown_content, file_name)


def write_last_run(counts, store_name):
    """Write log artefacts to last_run.txt."""
    lines = [
        "=== JOB LOG COUNTS ===",
        f"Store: {store_name}",
        f"Added: {counts['added']}",
        f"Updated: {counts['updated']}",
        f"Skipped: {counts['skipped']}",
    ]
    
    output = "\n".join(lines)
    print(f"\n{output}")
    with open("last_run.txt", "w", encoding="utf-8") as f:
        f.write(output + "\n")


def main():
    ARTICLE_COUNT = 100 # at least 30
    
    # TASK 1: Scrape ⇒ Markdown 
    articles = get_articles(get_articles_api_url(), ARTICLE_COUNT)
    
    # TASK 2: Build AI Assistant & Programmatically Load Vector Store 
    client = get_client()
    file_search_store = get_or_create_file_search_store(client, "OptiSigns Search Store")
    
    # TASK 2, 3: Daily job 
    counts = sync_articles_to_store(client, file_search_store, articles)
    write_last_run(counts, file_search_store.name)


if __name__ == "__main__":
    main()
