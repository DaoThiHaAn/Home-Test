import os
import re
import dotenv
from google import genai


dotenv.load_dotenv()

DEFAULT_ARTICLES_API_URL = "https://support.optisigns.com/api/v2/help_center/articles.json"


def get_articles_api_url() -> str:
    return DEFAULT_ARTICLES_API_URL


def get_client():
    return genai.Client()


def get_desc_updated_articles_api_url():
    return f'{DEFAULT_ARTICLES_API_URL}?sort_by=updated_at&sort_order=desc'


def create_file_name(title, unix_timestamp):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{slug}_{unix_timestamp}.md"
