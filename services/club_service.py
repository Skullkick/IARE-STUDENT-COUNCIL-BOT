from keyboards import club_event_keyboards
from utils import sqlitedb

async def add_club_details(bot, chat_id):
    field_presence_dictionary = await sqlitedb.check_temp_club_field_presence(chat_id)
    
    # Check each field and prompt for missing details
    if not field_presence_dictionary["name"]:
        await bot.send_message(chat_id, "Send the name of the club")
    elif not field_presence_dictionary["description"]:
        await bot.send_message(chat_id, "Send the description of the club")
    elif not field_presence_dictionary["president"]:
        await bot.send_message(chat_id, "Send the name of the president of the club")
    elif not field_presence_dictionary["vice_president"]:
        await bot.send_message(chat_id, "Send the name of the vice president of the club")
    else:
        # All fields are filled, proceed to confirmation or next step
        await bot.send_message(chat_id, "All club details are complete. Thank you!")
