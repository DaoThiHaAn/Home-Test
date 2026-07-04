import dotenv
import os
from google import genai
from google.genai import types


dotenv.load_dotenv()

def get_articles_api_url():
    return os.getenv("ARTICLES_API")

def get_client():
    return genai.Client() # auto uses GEMINI_API_KEY from environment variable

def get_incremental_articles_api_url(last_timestamp):
    return f"{os.getenv("INCREMENTAL_ARTICLES_API")}{last_timestamp}"

def create_file_name(title, unix_timestamp):
    slug = title.lower().replace(" ", "-").replace("/", "-")
    return f"{slug}_{unix_timestamp}.md"