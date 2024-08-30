from pyrogram import Client,filters
import asyncio



BOT_TOKEN = ""
API_ID = ""
API_HASH = ""


bot = Client(
    bot_token=BOT_TOKEN,
    api_id= API_ID,
    api_hash= API_HASH
)


@bot.on_callback_query()
async def callback_query_handler(bot,callback_query):
    # club and event management query handler
    # File upload and Management query handler
    # Contact information and request handler
    # Reminders and Notifications
    # Meeting management 
    # Administrative tools
    pass


if "__name__" == "__main__":
    bot.run()