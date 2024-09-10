# This is the main entry point for the bot.
from pyrogram import Client,filters
import config
from templates import club_events
from keyboards import club_event_keyboards

bot = Client(
        "IARE BOT",
        bot_token = config.BOT_TOKEN,
        api_id = config.API_ID,
        api_hash = config.API_HASH
)

@bot.on_message(filters.command(commands=["event"]))
async def start_event_handler(bot,message):
    pass

@bot.on_message(filters.command(commands=["clubs"]))
async def start_clubs(bot,message):
    await message.reply_text(club_events.ADD_CLUB_EVENT[0],reply_markup = club_event_keyboards.add_view_clubs_button)

@bot.on_message(filters.private&filters.text)
async def recieve_inputs(bot,message):
     pass