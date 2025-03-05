import requests
from bs4 import BeautifulSoup
from config import LOGGER, BASE_URLS
from utils import load_processed_movies, save_processed_movies

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
}

def TheBongPirate1():
    base_url = BASE_URLS["site1"]
    response = requests.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        LOGGER.error(f"Failed to fetch {base_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    recent_section = soup.find("h2", class_="widget-title", string="Recent and Updated Movies")
    if not recent_section:
        LOGGER.error("Recent movies section not found.")
        return []

    movie_list = recent_section.find_next("ul")
    if not movie_list:
        LOGGER.error("Movie list not found.")
        return []

    movies = []
    for li in movie_list.find_all("li"):
        a_tag = li.find("a")
        if a_tag:
            title = a_tag.text.strip()
            movie_url = a_tag["href"]
            if not movie_url.startswith("http"):
                movie_url = base_url.rstrip("/") + "/" + movie_url.lstrip("/")
            movies.append({"title": title, "url": movie_url})

    return movies

def TheBongPirate_Magnets1(movie_url):
    response = requests.get(movie_url, headers=HEADERS)
    if response.status_code != 200:
        LOGGER.error(f"Failed to fetch {movie_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    return [a["href"] for a in soup.select('a[href^="magnet:?xt="]')]
