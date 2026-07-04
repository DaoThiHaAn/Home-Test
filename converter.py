"""Convert OptiSigns support articles in json format to .md"""

from markdownify import markdownify
from datetime import datetime
from utils import create_file_name

FILE_PATH = "articles_markdown"

def convert_article_to_markdown(article):
    title = article["title"]
    body = article["body"]
    url = article["html_url"]
    updated_at = article["updated_at"]  # Timestamp format: 2026-07-02T14:16:18Z
    unix_timestamp = int(
        datetime.fromisoformat(updated_at.replace("Z", "+00:00")).timestamp()
    )
    
    content = f"""
# {title}
**URL:** [{url}]({url}) # preserve the link to the original article
**Updated:** {updated_at}
{body}
    """
    markdown_content = markdownify(content)
    file_name = create_file_name(title, unix_timestamp)
    
    return markdown_content, file_name
                
            
def save_markdown_to_file(file_content, file_name):
    filename = f"{FILE_PATH}/{file_name}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
        
    print(f"Saved markdown file: {filename}")
    return filename
