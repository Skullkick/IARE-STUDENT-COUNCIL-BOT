from utils import sqlitedb
from templates import council_templates
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
CLUB_NAMES_TEXT = "Select the clubs to start an event"
EVENT_NAMES_TEXT = "Select the event to view or delete"
ADD_CLUBS = ("Click on Add Club to add a club or view to view a club","testing")
"""Add Events
[0] Starting page of adding or viewing event
[1] To choose the date and submit the date
[2] To choose the time and submit the time
[3] To select the type of event
"""

ADD_EVENTS = ("Click on add event or view event.","Choose the date and click on submit","Choose the time and click on submit","Select the type of event.","All the details of the event has been saved","Edited details have been saved.")
ADD_EVENT_DATA = ("Send the report of the event.","Send the proposal form pdf of the event.","Send the flyer and schedule in a pdf.","Send the list of participants pdf.",
"The link has been successfully stored and sent to the student council admins.",
"The PDF has been successfully delivered to the admins.",
"Please send the reporter's name and contact in the following format:\n\n reporter_name:reporter_number","Successfully added reporters_name and number.")

async def start_club_buttons(bot,chat_id):
    club_info  = await sqlitedb.get_club_info_by_chat_id(chat_id=chat_id)
    club_id = club_info['id']
    club_name = club_info["name"]
    text = await council_templates.generate_club_info_text_single_message(club_info)
    buttons = []
    buttons.append(InlineKeyboardButton("EVENTS",callback_data=f"EVENT-club_event-{club_name}-{club_id}"))
    buttons = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await bot.send_message(chat_id,text,reply_markup=buttons)