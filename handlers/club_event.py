# this file contains the source code to manage the events that are conducted by the clubs
from templates import club_events
from keyboards import club_event_keyboards
from utils import sqlitedb

async def start_clubs_buttons(bot,message):
    """
    This Function is used to start the user buttons with the text.
    :param bot: Client session
    :param message: Message of the user"""
    clubs_buttons = club_event_keyboards.clubs_buttons
    await message.reply_text(club_events.CLUB_NAMES_TEXT,reply_markup = clubs_buttons)


async def recieve_club_info(bot,message):
    chat_id = message.chat.id
    fields_status = await sqlitedb.check_temp_club_field_presence(chat_id)
    # Check if message contains text
    if message.text:
        text = message.text
        
        # Update the 'name' field if it's False
        if not fields_status['name']:
            await sqlitedb.store_temp_club_info(chat_id,name=text)
            await message.reply_text(f"Name has been set to: {text}")
        # Update the 'description' field if 'name' is True and 'description' is False
        elif not fields_status['description']:
            await sqlitedb.store_temp_club_info(chat_id,description=text)
            await message.reply_text(f"Description has been set to: {text}")
        # Update the 'president' field if 'description' is True and 'president' is False
        elif not fields_status['president']:
            await sqlitedb.store_temp_club_info(chat_id,president=text)
            await message.reply_text(f"President has been set to: {text}")
        # Update the 'vice_president' field if 'president' is True and 'vice_president' is False
        elif not fields_status['vice_president']:
            await sqlitedb.store_temp_club_info(chat_id,vice_president=text)
            await message.reply_text(f"Vice President has been set to: {text}")
        else:
            await message.reply_text("All fields have been set.")