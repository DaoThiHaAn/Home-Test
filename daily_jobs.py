"""Daily jobs to update the articles in the database."""

from utils import get_incremental_articles_api_url
from scrapper import get_articles
from converter import convert_article_to_markdown, save_markdown_to_file
from uploader import upload_markdown_files_to_gemini
import os


def daily_jobs(client, file_search_store):
    existing_articles = client.file_search_stores.documents.list(parent=f"fileSearchStores/{file_search_store.name}")
    store_state = {}  #{slug: {name: str, timestamp: int}}
    timestamps = []
    
    # Get the most recent timestamp in Unix format from the existing articles
    for article in existing_articles:
        a_slug, a_timestamp = article.display_name.rsplit("_", 1)
        store_state[a_slug] = {"name": article.display_name, "timestamp": a_timestamp}
        timestamps.append(a_timestamp)
        
    most_recent_timestamp = max(timestamps) 
    incremental_api_url = get_incremental_articles_api_url(most_recent_timestamp)
    
    # Fetch only newly-updated articles from the incremental API
    newly_updated_articles = get_articles(incremental_api_url)
    
    added_count = 0
    updated_count = 0
    skipped_count = 0
    
    for article in newly_updated_articles:
        markdown_content, file_name = convert_article_to_markdown(article)
        slug, unix_timestamp = file_name.rsplit("_", 1)
        
        # Temporarily save the .md file
        temp_filename = save_markdown_to_file(markdown_content, file_name)
        
        # Check state of .md file
        if slug not in store_state:
            # New article, add it to the store
            added_count += 1
            
        else:
            # Updated article, delete old version from the File Search Store
            updated_count += 1
            client.file_search_stores.documents.delete(
                name = f"fileSearchStores/{file_search_store.name}/documents/{store_state[slug]['name']}_{store_state[slug]['timestamp']}.md",
                config = {"force": True}
            )
         
        # Upload new file File Search Store   
        upload_markdown_files_to_gemini(client, f"articles_markdown/{file_name}", file_search_store.name)
        
        # Delete the temporary .md file after uploading
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    
    skipped_count = len(store_state) - updated_count
    
    print("\n=== JOB LOG COUNTS ===")
    print(f"Added: {added_count}")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print("=======================")
    