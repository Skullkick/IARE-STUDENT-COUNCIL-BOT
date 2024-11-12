# This is the main entry point for the bot.
from pyrogram import Client,filters
# import config
from templates import club_events_templates,council_templates
from handlers import club_event_handler,council_members,file_uploads
from keyboards import club_event_keyboards,student_council_keyboard
from services import student_council_service
from utils import sqlitedb,sync_databases,PostgresSQL
import asyncio,os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
bot = Client(
        "STUDENT COUNCIL BOT",
        bot_token = BOT_TOKEN,
        api_id = API_ID,
        api_hash = API_HASH
)

# @bot.on_message(filters.command(commands=["event"]))
async def start_event_handler(bot,message):
    chat_id = message.chat.id
    if await sqlitedb.check_permission(chat_id,events=True) is True:
        await sqlitedb.delete_temp_event_by_chat_id(chat_id)
    await message.reply_text(club_events_templates.ADD_EVENTS[0],reply_markup = club_event_keyboards.add_view_events_button)

@bot.on_message(filters.command(commands="authorize"))
async def authorize_and_add_admin(bot,message):
    await council_members.add_admin_by_authorization(bot, message)
    
@bot.on_message(filters.command(commands="admin"))
async def admin_buttons(bot,message):
    chat_id = message.chat.id
    admin_chat_ids = await sqlitedb.get_all_student_council_chat_ids()
    field_presence = await sqlitedb.check_student_council_field_presence(chat_id)
    if chat_id in admin_chat_ids:
        if field_presence['all_values'] is False:
            await sqlitedb.set_permissions(chat_id=chat_id,council_admin=True)
            await student_council_service.add_student_council_details(bot,chat_id)
        await council_templates.start_student_council_buttons(bot, message)

@bot.on_message(filters.command(commands=["start"]))
async def start_buttons(bot,message):
    chat_id = message.chat.id
    council_admin_chat_ids = await sqlitedb.get_all_student_council_chat_ids()
    club_chat_ids = await sqlitedb.get_pres_and_vice_pres_chat_ids()
    enforcement_team_chat_ids = await sqlitedb.get_enforcement_team_chat_ids()
    core_member_chat_ids = await sqlitedb.get_core_member_chat_ids()
    if chat_id in council_admin_chat_ids:
        await council_templates.start_student_council_buttons(bot,message)
    elif chat_id in club_chat_ids:
        await club_events_templates.start_club_buttons(bot,chat_id=chat_id)
    elif chat_id in enforcement_team_chat_ids:
        await council_templates.start_enforcement_member_buttons(bot,chat_id)
    elif chat_id in core_member_chat_ids:
        # print("starting core member dashboard")
        await council_templates.start_core_member_buttons(bot,message)
    else:
        await bot.send_message(chat_id,"You are not a member of this bot.")

# @bot.on_message(filters.command(commands=["clubs"]))
async def start_clubs(bot,message):
    chat_id = message.chat.id
    if await sqlitedb.check_permission(chat_id,clubs=True) is True:
        await sqlitedb.delete_temp_club_by_chat_id(chat_id)
    await message.reply_text(club_events_templates.ADD_CLUBS[0],reply_markup = club_event_keyboards.add_view_clubs_button)

@bot.on_message(filters.private&filters.text)
async def recieve_inputs(bot,message):
    chat_id = message.chat.id # chat id of a user
    # Conditional statements to process text based on the permission
    if await sqlitedb.check_permission(chat_id,clubs=True) is True:
        await club_event_handler.recieve_club_info(bot,message)
    elif await sqlitedb.check_permission(chat_id, edit_clubs=True):
        await club_event_handler.recieve_edit_club_info(bot,message)
    elif await sqlitedb.check_permission(chat_id,events=True) is True:
        await club_event_handler.recieve_events_info(bot,message)
    elif await sqlitedb.check_permission(chat_id,edit_events=True):
        await club_event_handler.recieve_edit_event_info(bot,message)
    elif await sqlitedb.check_permission(chat_id,core_team=True) is True:
        await council_members.receive_core_info(bot,message)
    elif await sqlitedb.check_permission(chat_id,edit_core=True):
        await council_members.receive_edit_core_info(bot,message)
    elif await sqlitedb.check_permission(chat_id,council_admin=True) is True:
        await council_members.recieve_council_admin_info(bot,message)
    elif await sqlitedb.check_permission(chat_id=chat_id,photos_drive_link=True):
        await file_uploads.recieve_link(bot,message)
    elif await sqlitedb.check_permission(chat_id=chat_id,reporter_details=True):
        event_id = await sqlitedb.check_permission(chat_id=chat_id,reporter_details=True)
        await club_event_handler.recieve_reporter_details(bot,message,event_id=event_id)
    elif await sqlitedb.check_permission(chat_id=chat_id,core_team_tasks=True):
        await council_members.recieve_tasks_core_team(bot,message=message)
    elif await sqlitedb.check_permission(chat_id=chat_id,enforcement_team=True):
        await council_members.recieve_enforcement_team_info(bot=bot,message=message)
       
@bot.on_message(filters.private & filters.document)
async def _download_pdf(bot,message):
    chat_id = message.chat.id # chat id of a user
    # Based on the permissions assigned downloads the pdf file.
    if await sqlitedb.check_permission(chat_id=chat_id,proposal_form=True):
        event_id = await sqlitedb.check_permission(chat_id=chat_id,proposal_form=True)
        await file_uploads.download_pdf(bot,message,options="proposal_form",event_id=event_id)
    elif await sqlitedb.check_permission(chat_id=chat_id,flyer=True):
        event_id = await sqlitedb.check_permission(chat_id=chat_id,flyer=True)
        await file_uploads.download_pdf(bot,message,options="flyer_schedule",event_id=event_id)
    elif await sqlitedb.check_permission(chat_id=chat_id,report_upload=True):
        event_id = await sqlitedb.check_permission(chat_id=chat_id,report_upload=True)
        await file_uploads.download_pdf(bot,message,options="report",event_id=event_id)
    elif await sqlitedb.check_permission(chat_id=chat_id,list_of_participants=True):
        event_id = await sqlitedb.check_permission(chat_id=chat_id,list_of_participants=True)
        await file_uploads.download_pdf(bot,message,options="list_of_participants",event_id=event_id)


@bot.on_callback_query()
async def callback_query(bot,callback_query):
    data_parts = callback_query.data.split("-") # Split the data into multiple parts to proccess
    if len(data_parts) > 1:
        if data_parts[0] == "CLUB":
            await club_event_keyboards.clubs_callback_function(bot,callback_query)
        elif data_parts[0]=="EVENT":
            await club_event_keyboards.events_callback_function(bot,callback_query)
        elif data_parts[0] == "COUNCIL":
            await student_council_keyboard.council_callback_function(bot=bot,callback_query=callback_query)
        elif data_parts[0] == "CORE":
            await student_council_keyboard.core_team_callback_function(bot=bot,callback_query=callback_query)
        elif data_parts[0] == "ENFT":
            await student_council_keyboard.enforcement_team_callback_function(bot,callback_query)


async def main(bot):
    await PostgresSQL.create_all_pgdatabase_tables()
    await sqlitedb.initialize_sqlite_database()
    await sync_databases.sync_databases()
    # Add subroutine for reminders function.


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(bot))
    bot.run()