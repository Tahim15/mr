from pyrogram import Client
from config import LOGGER

async def some_plugin_function(client: Client, message):
    LOGGER(__name__).info(f"Received message: {message.text}")
    await message.reply_text("This is a plugin response!")
