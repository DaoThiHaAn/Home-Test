"""Convert OptiSigns support articles from JSON to Markdown."""

from datetime import datetime
from pathlib import Path

from markdownify import markdownify

from utils import create_file_name


ARTICLES_DIR = Path("articles_markdown")


def convert_article_to_markdown(article):
    title = article["title"]
    body = article["body"]
    url = article["html_url"]
    updated_at = article["updated_at"]
    unix_timestamp = int(
        datetime.fromisoformat(updated_at.replace("Z", "+00:00")).timestamp()
    )

    content = f"""\
# {title}

Article URL: {url}

**Updated:** {updated_at}

{body}
"""
    markdown_content = markdownify(content)
    file_name = create_file_name(title, unix_timestamp)

    return markdown_content, file_name


def save_markdown_to_file(file_content, file_name):
    ARTICLES_DIR.mkdir(exist_ok=True)
    filename = ARTICLES_DIR / file_name
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)

    print(f"Saved markdown file: {filename}")
    return str(filename)
