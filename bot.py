# This is the main entry point for the bot.
from pyrogram import Client
import config

bot = Client(
        "IARE BOT",
        bot_token = config.BOT_TOKEN,
        api_id = config.API_ID,
        api_hash = config.API_HASH
)