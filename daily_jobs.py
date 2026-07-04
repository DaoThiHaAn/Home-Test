"""Daily sync logic for OptiSigns articles."""

from converter import convert_article_to_markdown, save_markdown_to_file
from uploader import upload_markdown_file_to_gemini


def _split_slug_and_timestamp(display_name):
    """ Split the file display name into slug and timestamp."""
    
    stem = display_name.removesuffix(".md")
    slug, timestamp = stem.rsplit("_", 1)
    return slug, int(timestamp)


def _existing_articles_by_slug(client, file_search_store):
    store_name = getattr(file_search_store, "name", file_search_store)

    state = {}

    print("File Search Store object:", file_search_store)
    
    for document in client.file_search_stores.documents.list(parent=store_name):
        display_name = getattr(document, "display_name", "")

        if not display_name.endswith(".md"):
            continue

        slug, timestamp = _split_slug_and_timestamp(display_name)

        state[slug] = {
            "document": document,  # Store the document object for potential deletion
            "timestamp": timestamp,
        }

    return state


def sync_articles_to_store(client, file_search_store, new_scrapped_articles):
    """Add the newly scraped articles to the Gemini File Search store, skipping unchanged articles."""
    
    # Get all existing articles in the store 
    existing_by_slug = _existing_articles_by_slug(client, file_search_store)

    counts = {
        "added": 0,
        "updated": 0,
        "skipped": 0,
    }

    embedded_count = 0
    for article in new_scrapped_articles:
        markdown_content, file_name = convert_article_to_markdown(article)

        slug, timestamp = file_name.rsplit("_", 1)
        timestamp = int(timestamp.removesuffix(".md"))

        existing = existing_by_slug.get(slug)

        # New article
        if existing is None:
            counts["added"] += 1

        # Unchanged
        elif timestamp == existing["timestamp"]:
            counts["skipped"] += 1
            continue

        # Updated
        else:
            counts["updated"] += 1

            # Delete the existing document from the store before uploading the new version
            client.file_search_stores.documents.delete(
                name=existing["document"].name,
                config={"force": True},
            )

        # Temporarily save the new .md file
        markdown_path = save_markdown_to_file(markdown_content, file_name)

        upload_markdown_file_to_gemini(
            client,
            markdown_path,
            file_search_store,
            file_number=embedded_count + 1
        )
        embedded_count += 1

    return counts