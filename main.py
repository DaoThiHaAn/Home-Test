"""One-shot scraper and Gemini File Search sync job."""

from converter import convert_article_to_markdown, save_markdown_to_file
from daily_jobs import sync_articles_to_store
from scrapper import get_articles
from uploader import get_or_create_file_search_store
from utils import  get_articles_api_url, get_desc_updated_articles_api_url, get_client
from datetime import datetime, timedelta

ARTICLE_COUNT = 50 # at least 30

def write_last_run(counts, store_name):
    """Write log artefacts to last_run.txt."""
    lines = [
        "=== JOB LOG COUNTS ===",
        f"Last run timestamp finished at: {datetime.now().isoformat()}",
        # f"Store: {store_name}",
        f"Added: {counts['added']}",
        f"Updated: {counts['updated']}",
        f"Skipped: {counts['skipped']}",
    ]
    
    output = "\n".join(lines)
    print(f"\n{output}")
    with open("last_run.txt", "w", encoding="utf-8") as f:
        f.write(output + "\n")

def retrieve_articles(is_first_run=False):
    if is_first_run:
        print("First run: Scraping articles and saving to markdown files.")
        return get_articles(get_articles_api_url(), ARTICLE_COUNT)

    # get all newly updated articles within the last 24 hours
    print("Daily run: Scraping only newly updated articles within the last 24 hours.")
    
    last_run_timestamp = int((datetime.now() - timedelta(days=1)).timestamp())
    desc_updated_articles = get_articles(get_desc_updated_articles_api_url())
    articles_to_sync = [article for article in desc_updated_articles if int(datetime.fromisoformat(article["updated_at"].replace("Z", "+00:00")).timestamp()) > last_run_timestamp]
    return articles_to_sync


def main():    
    client = get_client()
    file_search_store, is_first_run = get_or_create_file_search_store(client, "OptiSigns Search Store")
    
    articles = retrieve_articles(is_first_run)
    counts = sync_articles_to_store(client, file_search_store, articles)
    write_last_run(counts, file_search_store.name)


if __name__ == "__main__":
    main()
