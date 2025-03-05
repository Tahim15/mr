import asyncio
from config import LOGGER, CHECK_INTERVAL, CHANNEL_ID
from utils import load_processed_movies, save_processed_movies
from sites.scrape_site1 import TheBongPirate1, TheBongPirate_Magnets1
from sites.scrape_site2 import TheBongPirate2, TheBongPirate_Magnets2

async def check_new_movies(client):
    processed_movies = load_processed_movies()

    while True:
        LOGGER.info("Checking for new movies...")

        movies = TheBongPirate1()
        if movies:
            for movie in movies:
                if movie["url"] in processed_movies:
                    LOGGER.info(f"Skipping already processed movie: {movie['title']}")
                    continue

                magnets = TheBongPirate_Magnets1(movie["url"])
                if magnets:
                    for link in magnets:
                        message = f"/ql {link}\n<b>Tag:</b> <code>@Mr_official_300</code> <code>2142536515</code>"
                        await client.send_message(CHANNEL_ID, message, disable_web_page_preview=True)

                    processed_movies.append(movie["url"])
                    save_processed_movies(processed_movies)

        movies = TheBongPirate2()
        if movies:
            for movie in movies:
                if movie["url"] in processed_movies:
                    LOGGER.info(f"Skipping already processed movie: {movie['title']}")
                    continue

                magnets = TheBongPirate_Magnets2(movie["url"])
                if magnets:
                    for link in magnets:
                        message = f"/ql {link}\n<b>Tag:</b> <code>@Mr_official_300</code> <code>2142536515</code>"
                        await client.send_message(CHANNEL_ID, message, disable_web_page_preview=True)

                    processed_movies.append(movie["url"])
                    save_processed_movies(processed_movies)

        await asyncio.sleep(CHECK_INTERVAL)
