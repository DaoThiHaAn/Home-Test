import os
import re
import dotenv
from google import genai


dotenv.load_dotenv()

def get_articles_api_url() -> str:
    return os.getenv("ARTICLES_API")


def get_client():
    return genai.Client()


def get_desc_updated_articles_api_url():
    return f'{os.getenv("ARTICLES_API")}?sort_by=updated_at&sort_order=desc'


def create_file_name(title, unix_timestamp):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{slug}_{unix_timestamp}.md"
