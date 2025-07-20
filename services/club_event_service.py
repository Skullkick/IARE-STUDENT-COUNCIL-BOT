from keyboards import club_event_keyboards
from utils import sqlitedb
from templates import club_events_templates
from handlers import club_event_handler
import datetime

async def add_club_details(bot, chat_id):
    field_presence_dictionary = await sqlitedb.check_temp_club_field_presence(chat_id)
    # Check each field and prompt for missing details
    if not field_presence_dictionary["name"]:
        await bot.send_message(chat_id, "Send the name of the club")
    elif not field_presence_dictionary["description"]:
        await bot.send_message(chat_id, "Send the description of the club")
    elif not field_presence_dictionary["president"]:
        await bot.send_message(chat_id, "Send the name of the president of the club")
    elif not field_presence_dictionary["pres_chat_id"]:
        await bot.send_message(chat_id, "Send the chat_id of president of the club")
    elif not field_presence_dictionary["vice_president"]:
        await bot.send_message(chat_id, "Send the name of the vice president of the club")
    elif not field_presence_dictionary["vice_pres_chat_id"]:
        await bot.send_message(chat_id, "Send the chat_id of vice president of the club")
    else:
        # All fields are filled, proceed to confirmation or next step
        if await sqlitedb.check_permission(chat_id=chat_id,clubs=True) is True:
            await sqlitedb.set_permissions(chat_id,clubs=False)
            await club_event_handler.initialize_storing_club_values(chat_id)
        elif await sqlitedb.check_permission(chat_id=chat_id,edit_clubs=True):
            await sqlitedb.set_permissions(chat_id=chat_id)
        await bot.send_message(chat_id, "All club details are complete. Thank you!")
        await bot.send_message(chat_id,club_events_templates.ADD_CLUBS[0],reply_markup = club_event_keyboards.add_view_clubs_button)


async def add_event_details(bot, chat_id):
    field_presence_dictionary = await sqlitedb.check_temp_event_field_presence(chat_id)
    # Check each field and prompt for missing details
    if not field_presence_dictionary["name"]:
        await bot.send_message(chat_id, "Send the name of the event")
    elif not field_presence_dictionary["number_of_days"]:
        await bot.send_message(chat_id, "Send the number of days for the event")
    elif not field_presence_dictionary["venue"]:
        # print(field_presence_dictionary)
        await bot.send_message(chat_id, "Send the venue of the event")
    elif not field_presence_dictionary["audience_size"]:
        await bot.send_message(chat_id, "Send the estimated audience size for the event")
    elif not field_presence_dictionary["date_time"]:
        # Get the current date
        # print(f"In date_time field presence is : {field_presence_dictionary}")
        current_date = datetime.date.today()
        current_day = current_date.day
        current_month = current_date.month
        current_year = current_date.year
        await bot.send_message(chat_id, "Select the date of the event.",reply_markup = await club_event_keyboards.generate_date_picker_buttons(method="EVENT",current_day=current_day,current_month=current_month,current_year=current_year))
    elif not field_presence_dictionary["type"]:
        await bot.send_message(chat_id, "Send the type of the event (Tech or Non-Tech)",reply_markup = club_event_keyboards.tech_nontech_event_button)
    else:
        # All fields are filled, proceed to confirmation or next step
        await bot.send_message(chat_id, "All event details are complete. Thank you!")


