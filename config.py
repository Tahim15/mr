import logging
import os

LOGGER = logging.getLogger(__name__)
CHECK_INTERVAL = 600

API_ID = int(os.getenv("API_ID", 123456))
API_HASH = os.getenv("API_HASH", "your_api_hash_here"))
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here"))

BASE_URLS = {
    "site1": os.getenv("BASE_URL_1", "https://www.5movierulz.tel/"),
    "site2": os.getenv("BASE_URL_2", "https://www.example-movie-site.com/"),
}

CHANNEL_ID = int(os.getenv("CHANNEL_ID", -1001234567890))
