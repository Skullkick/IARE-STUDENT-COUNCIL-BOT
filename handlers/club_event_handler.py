# this file contains the source code to manage the events that are conducted by the clubs
from templates import club_events_templates
from keyboards import club_event_keyboards
from services import club_event_service
from utils import sqlitedb,time,PostgresSQL

async def start_clubs_buttons(bot,message):
    """
    This Function is used to start the user buttons with the text.
    :param bot: Client session
    :param message: Message of the user
    """
    clubs_buttons = club_event_keyboards.clubs_buttons
    await message.reply_text(club_events_templates.CLUB_NAMES_TEXT,reply_markup = clubs_buttons)

async def is_valid_integer(text):
    if isinstance(text, int):
        return True
    elif isinstance(text, str):
        try:
            int(text)
            return True
        except ValueError:
            return False
    return False

async def initialize_storing_club_values(chat_id):
    try:
        # Retrieve temporary club data
        temp_chat_id, temp_club_id, club_name, club_description, club_president, pres_chat_id, club_vice_president, vice_pres_chat_id = await sqlitedb.retrieve_temp_club_info_by_chat_id(chat_id)
        
        # Store the club information
        if await sqlitedb.store_club_info(
            name=club_name,
            description=club_description,
            president=club_president,
            pres_chat_id=pres_chat_id,
            vice_president=club_vice_president,
            vice_pres_chat_id=vice_pres_chat_id
        ):
        
            # If storage is successful, delete the temporary entry
            await PostgresSQL.store_club_info(
                name=club_name,
                description=club_description,
                president=club_president,
                pres_chat_id=pres_chat_id,
                vice_president=club_vice_president,
                vice_pres_chat_id=vice_pres_chat_id
            )
            await sqlitedb.delete_temp_club_by_chat_id(chat_id)

        
    except Exception as e:
        print(f"Error storing Club info to the database: {e}")

async def store_edited_club_values(chat_id):
    try:
        temp_chat_id,temp_club_id,club_name,club_description,club_president,pres_chat_id,club_vice_president,vice_pres_chat_id = await sqlitedb.retrieve_temp_club_info_by_chat_id(chat_id)
        await sqlitedb.store_club_info(
            club_id=temp_club_id,name=club_name,
            description=club_description,
            president=club_president,
            vice_president=club_vice_president
            )
        await PostgresSQL.store_club_info(
            club_id=temp_club_id,name=club_name,
            description=club_description,
            president=club_president,
            vice_president=club_vice_president
        )
        await sqlitedb.delete_temp_club_by_chat_id(chat_id)

    except Exception as  e:
        print(f"Error storing the values to the database : {e}")

async def store_edited_event_values(chat_id):
    try:
        stored_chat_id,stored_event_id, event_name, event_no_of_days, event_date_time, event_venue, event_audience_size, event_type, club_id = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id)
        await sqlitedb.store_event_info(
            id=stored_event_id,
            name=event_name,
            number_of_days=event_no_of_days,
            date_time=event_date_time,
            venue = event_venue,
            audience_size=event_audience_size,
            type=event_type,
            club_id=club_id 
        )
        await PostgresSQL.store_event_info(
            id=stored_event_id,
            name=event_name,
            number_of_days=event_no_of_days,
            date_time=event_date_time,
            venue = event_venue,
            audience_size=event_audience_size,
            type=event_type,
            club_id=club_id  
        )
        await sqlitedb.delete_temp_event_by_chat_id(chat_id)
        #Get the event details by event_id 
        event_details = await sqlitedb.get_event_info_by_id(event_id=stored_event_id)
        _,event_name,number_of_days,date_time,venue,audience_size,type_of_event = event_details
        event_date = date_time.split("-")[0]
        proposal_form_date = await time.modify_event_date(event_date=event_date,num_of_days=-1)
        flyer_and_schedule_date = await time.modify_event_date(event_date=event_date,num_of_days=-1)
        list_of_participants_date = event_date
        report_upload_date = await time.modify_event_date(event_date=event_date,num_of_days=2)
        photos_upload_date = await time.modify_event_date(event_date=event_date,num_of_days=2)
        proposal_form =proposal_form_date + "-not_submitted"
        flyer_and_schedule = flyer_and_schedule_date+"-not_submitted"
        list_of_participants = list_of_participants_date + "-not_submitted"
        report_upload = report_upload_date + "-not_submitted"
        photos_upload = photos_upload_date+"-not_submitted"
        await sqlitedb.store_or_update_event_data(event_id=stored_event_id,photos_link=photos_upload,event_report=report_upload,proposal_form=proposal_form,flyer_and_schedule=flyer_and_schedule,list_of_participants=list_of_participants)
        await PostgresSQL.store_or_update_event_data(event_id=stored_event_id,
                                                  photos_link=photos_upload,
                                                  event_report=report_upload,
                                                  proposal_form=proposal_form,
                                                  flyer_and_schedule=flyer_and_schedule,
                                                  list_of_participants=list_of_participants
                                                  )
    except Exception as  e:
        print(f"Error storing the values to the database : {e}")


async def initialize_storing_event_values(chat_id):
    # try:
    # Retrieve temporary event information from the database
    temp_chat_id, temp_event_id, event_name, number_of_days, date_time, venue, audience_size, type_of_event,club_id = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id)
    
    # Store the event information into the main events table (replace with appropriate table and logic)
    if await sqlitedb.store_event_info(
        id=None, 
        name=event_name,
        number_of_days=number_of_days,
        date_time=date_time,
        venue=venue,
        audience_size=audience_size,
        type=type_of_event,
        club_id=club_id
    ):
    
        # After storing the event information, delete it from the temporary table
        event_name = event_name
        await sqlitedb.delete_temp_event_by_chat_id(chat_id)
        await PostgresSQL.store_event_info(        
            id=None, 
            name=event_name,
            number_of_days=number_of_days,
            date_time=date_time,
            venue=venue,
            audience_size=audience_size,
            type=type_of_event,
            club_id=club_id
            )
        # print("Successfully deleted temp event by chat_id")
    # Get the event id to set the date for event_data
    event_id = await sqlitedb.get_event_id_by_name(event_name=event_name)
    #Get the event details by event_id 
    if event_id:
        event_details = await sqlitedb.get_event_info_by_id(event_id=event_id)
        # print(event_details)
        _,event_name,number_of_days,date_time,venue,audience_size,type_of_event,club_id = event_details
        event_date = date_time.split("-")[0]
        proposal_form_date = await time.modify_event_date(event_date=event_date,num_of_days=-1)
        flyer_and_schedule_date = await time.modify_event_date(event_date=event_date,num_of_days=-1)
        list_of_participants_date = event_date
        report_upload_date = await time.modify_event_date(event_date=event_date,num_of_days=2)
        photos_upload_date = await time.modify_event_date(event_date=event_date,num_of_days=2)
        proposal_form =proposal_form_date + "-not_submitted"
        flyer_and_schedule = flyer_and_schedule_date+"-not_submitted"
        list_of_participants = list_of_participants_date + "-not_submitted"
        report_upload = report_upload_date + "-not_submitted"
        photos_upload = photos_upload_date+"-not_submitted"
        await sqlitedb.store_or_update_event_data(event_id=event_id,photos_link=photos_upload,event_report=report_upload,proposal_form=proposal_form,flyer_and_schedule=flyer_and_schedule,list_of_participants=list_of_participants)
        await PostgresSQL.store_or_update_event_data(event_id=event_id,photos_link=photos_upload,event_report=report_upload,proposal_form=proposal_form,flyer_and_schedule=flyer_and_schedule,list_of_participants=list_of_participants)
    # except Exception as e:
    #     print(f"Error storing the event values to the database: {e}")


async def recieve_club_info(bot,message):
    chat_id = message.chat.id
    fields_status = await sqlitedb.check_temp_club_field_presence(chat_id)
    # Check if message contains text
    if message.text:
        text = message.text
        # Update the 'name' field if it's False
        if not fields_status['name']:
            await sqlitedb.store_temp_club_info(chat_id,name=text)
            # await message.reply_text(f"Name has been set to: {text}")
            # await initialize_storing_club_values(chat_id)
            await club_event_service.add_club_details(bot,chat_id)
        # Update the 'description' field if 'name' is True and 'description' is False
        elif not fields_status['description']:
            await sqlitedb.store_temp_club_info(chat_id,description=text)
            # await message.reply_text(f"Description has been set to: {text}")
            # await initialize_storing_club_values(chat_id)
            await club_event_service.add_club_details(bot,chat_id)
        # Update the 'president' field if 'description' is True and 'president' is False
        elif not fields_status['president']:
            await sqlitedb.store_temp_club_info(chat_id,president=text)
            # await message.reply_text(f"President has been set to: {text}")
            # await initialize_storing_club_values(chat_id)
            await club_event_service.add_club_details(bot,chat_id)
        elif not fields_status['pres_chat_id']:
            if await is_valid_integer(text) is False:
                await bot.send_message(chat_id,"Chat ID is a numeric value. Please enter the value again.")
                return
            await sqlitedb.store_temp_club_info(chat_id=chat_id,pres_chat_id=int(text))
            await club_event_service.add_club_details(bot,chat_id)
        # Update the 'vice_president' field if 'president' is True and 'vice_president' is False
        elif not fields_status['vice_president']:
            await sqlitedb.store_temp_club_info(chat_id,vice_president=text)
            # await message.reply_text(f"Vice President has been set to: {text}")
            await club_event_service.add_club_details(bot,chat_id)
        elif not fields_status['vice_pres_chat_id']:
            if await is_valid_integer(text) is False:
                await bot.send_message(chat_id,"Chat ID is a numeric value. Please enter the value again.")
                return
            await sqlitedb.store_temp_club_info(chat_id=chat_id,vice_pres_chat_id=int(text),club_id=1) # Club id is for name sake here.
            await club_event_service.add_club_details(bot,chat_id)
        else:
            await message.reply_text("All fields have been set.")

async def recieve_edit_club_info(bot,message):
    chat_id = message.chat.id
    edit_action = await sqlitedb.check_permission(chat_id, edit_clubs=True)
    if edit_action == "name":
        text = message.text
        if text:
            await sqlitedb.store_temp_club_info(chat_id, name=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_club_values(chat_id)
            await message.reply_text(f"Name has been set to: {text}")
    elif edit_action == "description":
        text = message.text
        if text:
            await sqlitedb.store_temp_club_info(chat_id, description=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_club_values(chat_id)
            await message.reply_text(f"Description has been set to: {text}")

    elif edit_action == "president":
        text = message.text
        if text:
            await sqlitedb.store_temp_club_info(chat_id, president=text)
            await sqlitedb.set_permissions(chat_id,edit_clubs="pres_chat_id")
            await store_edited_club_values(chat_id)
            await message.reply_text(f"President has been set to: {text}")

    elif edit_action == "pres_chat_id":
        text = message.text
        if text:
            await sqlitedb.store_temp_club_info(chat_id, president=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_club_values(chat_id)
            await message.reply_text(f"President chat_id has been set to: {text}")

    elif edit_action == "vice_president":
        text = message.text
        if text:
            await sqlitedb.store_temp_club_info(chat_id, vice_president=text)
            await sqlitedb.set_permissions(chat_id,edit_clubs="vice_pres_chat_id")
            await message.reply_text(f"Vice President has been set to: {text}")
            await store_edited_club_values(chat_id)

    elif edit_action == "vice_pres_chat_id":
        text = message.text
        if text:
            await sqlitedb.store_temp_club_info(chat_id, president=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_club_values(chat_id)
            await message.reply_text(f"Vice President chat_id has been set to: {text}")         


async def recieve_events_info(bot,message):
    chat_id = message.chat.id
    fields_status = await sqlitedb.check_temp_event_field_presence(chat_id)
    # Check if the message contains text
    if message.text:
        text = message.text
        # Update the 'name' field if it's False
        if not fields_status['name']:
            await sqlitedb.store_temp_event_info(chat_id=chat_id, name=text)
            await club_event_service.add_event_details(bot, chat_id)
        # Update the 'number_of_days' field if 'name' is True and 'number_of_days' is False
        elif not fields_status['number_of_days']:
            if await is_valid_integer(text) is False:
                await bot.send_message(chat_id,"Number of days Should be numeric value.")
                return
            await sqlitedb.store_temp_event_info(chat_id=chat_id, number_of_days=text)
            await club_event_service.add_event_details(bot, chat_id)
        # Update the 'venue' field if 'date_time' is True and 'venue' is False
        elif not fields_status['venue']:
            await sqlitedb.store_temp_event_info(chat_id=chat_id, venue=text)
            await club_event_service.add_event_details(bot, chat_id)
        # Update the 'audience_size' field if 'venue' is True and 'audience_size' is False
        elif not fields_status['audience_size']:
            await sqlitedb.store_temp_event_info(chat_id=chat_id, audience_size=text)
            await sqlitedb.set_permissions(chat_id=chat_id, events=False)
            await club_event_service.add_event_details(bot, chat_id)
        # Update the 'date_time' field if 'number_of_days' is True and 'date_time' is False
        elif not fields_status['date_time']:
            await sqlitedb.store_temp_event_info(chat_id=chat_id, date_time=text)
            await club_event_service.add_event_details(bot, chat_id)

        # Update the 'type' field if 'audience_size' is True and 'type' is False
        elif not fields_status['type']:
            await sqlitedb.store_temp_event_info(chat_id=chat_id, type=text)
            await club_event_service.add_event_details(bot, chat_id)
            await initialize_storing_event_values(chat_id)
        else:
            await message.reply_text("All fields have been set.")

async def recieve_edit_event_info(bot, message):
    chat_id = message.chat.id
    edit_action = await sqlitedb.check_permission(chat_id, edit_events=True)
    # print(bool(edit_action))
    if edit_action == "name":
        text = message.text
        if text:
            await sqlitedb.store_temp_event_info(chat_id, name=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_event_values(chat_id)
            await message.reply_text(f"Name has been set to: {text}")

    elif edit_action == "number_of_days":
        text = message.text
        if text.isdigit():
            number_of_days = int(text)
            await sqlitedb.store_temp_event_info(chat_id, number_of_days=number_of_days)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_event_values(chat_id)
            await message.reply_text(f"Number of days has been set to: {number_of_days}")
        else:
            await message.reply_text("Please enter a valid number of days.")

    # elif edit_action == "date_time":
    #     text = message.text
    #     if text:
    #         await sqlitedb.store_temp_event_info(chat_id, date_time=text)
    #         await sqlitedb.set_permissions(chat_id)
    #         await store_edited_event_values(chat_id)
    #         await message.reply_text(f"Date and time has been set to: {text}")

    elif edit_action == "venue":
        text = message.text
        if text:
            await sqlitedb.store_temp_event_info(chat_id, venue=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_event_values(chat_id)
            await message.reply_text(f"Venue has been set to: {text}")

    elif edit_action == "audience_size":
        text = message.text
        if text.isdigit():
            audience_size = int(text)
            await sqlitedb.store_temp_event_info(chat_id, audience_size=audience_size)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_event_values(chat_id)
            await message.reply_text(f"Audience size has been set to: {audience_size}")
        else:
            await message.reply_text("Please enter a valid audience size.")

    # elif edit_action == "type":
    #     text = message.text
    #     if text:
    #         await sqlitedb.store_temp_event_info(chat_id, type=text)
    #         await sqlitedb.set_permissions(chat_id)
    #         await store_edited_event_values(chat_id)
    #         await message.reply_text(f"Event type has been set to: {text}")

async def recieve_reporter_details(bot,message,event_id):
    chat_id = message.chat.id
    if message.text:
        text = message.text.split(":")
        if text:
            if len(text) == 1:
                await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[6])
                return
            await sqlitedb.store_or_update_event_data(event_id=event_id,reporter_name=text[0],reporter_number=text[1])
            await PostgresSQL.store_or_update_event_data(event_id=event_id,reporter_name=text[0],reporter_number=text[1])
            await sqlitedb.set_permissions(chat_id)
            await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[7])