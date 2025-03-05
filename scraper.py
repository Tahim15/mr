import asyncio
import requests
from bs4 import BeautifulSoup
from config import LOGGER, CHECK_INTERVAL, CHANNEL_ID
from pyrogram import Client

BASE_URL = "https://www.5movierulz.tel/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
}

def get_recent_movies():
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        LOGGER(__name__).error("Failed to fetch the website.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    recent_section = soup.find("h2", class_="widget-title", string="Recent and Updated Movies")
    if not recent_section:
        LOGGER(__name__).error("Recent movies section not found.")
        return []

    movie_list = recent_section.find_next("ul")
    if not movie_list:
        LOGGER(__name__).error("Movie list not found.")
        return []

    movies = []
    for li in movie_list.find_all("li"):
        a_tag = li.find("a")
        if a_tag:
            title = a_tag.text.strip()
            movie_url = a_tag["href"]
            if not movie_url.startswith("http"):
                movie_url = BASE_URL.rstrip("/") + "/" + movie_url.lstrip("/")
            movies.append({"title": title, "url": movie_url})

    return movies

def get_magnet_links(movie_url):
    response = requests.get(movie_url, headers=HEADERS)
    if response.status_code != 200:
        LOGGER(__name__).error(f"Failed to fetch {movie_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    return [a["href"] for a in soup.select('a[href^="magnet:?xt="]')]

async def check_new_movies(client: Client):
    while True:
        LOGGER(__name__).info("Checking for new movies...")
        movies = get_recent_movies()

        if not movies:
            LOGGER(__name__).info("No recent movies found.")
        else:
            for movie in movies:
                magnets = get_magnet_links(movie["url"])
                if magnets:
                    message = f"<b>🎬 {movie['title']}</b>\n\n🔗 <a href='{movie['url']}'>Watch Here</a>\n\n"
                    message += "\n".join([f"<code>{link}</code>" for link in magnets])
                    await client.send_message(CHANNEL_ID, message, disable_web_page_preview=True)
                else:
                    LOGGER(__name__).info(f"No magnet links found for {movie['title']}")

        await asyncio.sleep(CHECK_INTERVAL)
