from pyrogram import Client
from config import LOGGER, CHECK_INTERVAL, CHANNEL_ID, API_ID, API_HASH, BOT_TOKEN
from scrapper import check_new_movies

app = Client(
    "my_movie_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def main():
    await app.start()
    await check_new_movies(app)
    await app.stop()

if __name__ == "__main__":
    app.run(main())
