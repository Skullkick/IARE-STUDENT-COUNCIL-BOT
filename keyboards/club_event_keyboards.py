from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from templates import club_events
from utils import sqlitedb
from services import club_service
# This file contains the keyboard code.

Cancel_event_button = [InlineKeyboardButton("Cancel",callback_data="cancel_event")]
back_to_clubs_button = [InlineKeyboardButton("Back",callback_data = "back_to_clubs")]
add_view_clubs_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Add Club",callback_data="add_club")],
        [InlineKeyboardButton("View Clubs",callback_data="view_clubs")]
    ]
)
async def clubs_buttons():
    """This function is used to generate the clubs buttons
    :param club_names: A tuple which will be containing all the club names.
    :returns: Returns buttons"""
    club_names_ids = await sqlitedb.get_club_names_and_indexes()
    Button = []
    for club_name,club_id in club_names_ids:
        Button.append([InlineKeyboardButton(f"{club_name}",callback_data=f"club_event-{club_name}-{club_id}")])
    Button = InlineKeyboardMarkup(
        inline_keyboard=Button
    )
    return Button


async def event_callback_function(bot,callback_query):
    """
    This Function performs operations based on the callback data from the user for the events.
    :param bot: Client session.
    :param callback_query: callback data of the user.

    :return: This returns nothing, But performs operations.
    """
    if "club_event" in callback_query.data:
        club_name = callback_query.data.split("-")[1]
        club_id = callback_query.data.split("-")[2]
        await callback_query.edit_message_text()
    elif callback_query.data == "back_to_clubs":
        await callback_query.answer()
        await callback_query.edit_message_text(
            club_events.CLUB_NAMES_TEXT,
            reply_markup = await clubs_buttons()
        )
    elif callback_query.data == "add_club":
        chat_id = callback_query.message.chat.id
        await callback_query.message.delete()
        await 

    
