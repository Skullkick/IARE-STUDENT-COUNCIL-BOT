from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from templates import club_events_templates,council_templates
from handlers import club_event_handler
from utils import sqlitedb,time
from services import club_event_service
import calendar
# import datetime
# This file contains the keyboard code.

Cancel_event_button = [InlineKeyboardButton("Cancel",callback_data="cancel_event")]
back_to_clubs_button = [InlineKeyboardButton("Back",callback_data = "CLUB-back_to_clubs")]
back_to_initial_clubs_button = [InlineKeyboardButton("Back",callback_data = "CLUB-back_to_initial_clubs")]
back_to_initial_events_button = [InlineKeyboardButton("Back", callback_data="EVENT-back_to_events_menu")]
add_view_clubs_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Add Club",callback_data="CLUB-add_club")],
        [InlineKeyboardButton("View Clubs",callback_data="CLUB-view_clubs")],
        [InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")]
    ]
)
# add_view_events_button = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton("Add Event", callback_data="EVENT-add_event")],
#         [InlineKeyboardButton("View Events", callback_data="EVENT-view_events")]
#     ]
# )

async def generate_club_event_buttons(club_id: int,back_button_to_view = False,chat_id = None):
    club_name = await sqlitedb.get_club_name_by_club_id(club_id=club_id)
    # print(club_name)
    if chat_id:
        # council_admin_chat_ids = await sqlitedb.get_all_student_council_chat_ids()
        club_chat_ids = await sqlitedb.get_pres_and_vice_pres_chat_ids()
        if chat_id in club_chat_ids:
                button = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton("Add Event", callback_data=f"EVENT-add_event-{club_id}")],
                        [InlineKeyboardButton("View Events", callback_data=f"EVENT-view_events-{club_id}")],
                        [InlineKeyboardButton("Back",callback_data=f"CLUB-club_member_dashboard-{club_name}-{club_id}")]
                    ]
                )
                return button
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Add Event", callback_data=f"EVENT-add_event-{club_id}")],
            [InlineKeyboardButton("View Events", callback_data=f"EVENT-view_events-{club_id}")],
            [InlineKeyboardButton("Back",callback_data=f"CLUB-club_detailed_view|edit-{club_name}-{club_id}")]
        ]
    )
    if back_button_to_view is True:
        button =[InlineKeyboardButton("Back",callback_data = f"EVENT-view_events-{club_id}")]
    return button

tech_nontech_event_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Tech", callback_data="EVENT-tech_event--")],
        [InlineKeyboardButton("Non Tech",callback_data="EVENT-non_tech_event--")]
    ]
)




async def generate_event_altering_receiving_buttons(event_id,event_name = None,chat_id = None):
    buttons = []
    club_id = await sqlitedb.get_club_id_by_event_id(event_id=event_id)
    # Retrieve the event data first
    event_data = await sqlitedb.retrieve_event_data(event_id)
    council_chat_ids = await sqlitedb.get_all_student_council_chat_ids()
    if event_data:
        # Extract the necessary fields from the retrieved data
        event_report_date_str = event_data.get('event_report').split("-")[0]  # Assuming this holds the event date
        proposal_form_date_str = event_data.get('proposal_form').split("-")[0]  # Assuming this holds the proposal form date
        flyer_and_schedule_date_str = event_data.get('flyer_and_schedule').split("-")[0]  # Assuming this holds flyer and schedule date
        list_of_participants_date_str = event_data.get('list_of_participants').split("-")[0]  # Assuming this holds the participants date

        # Create buttons based on date checks
        if await time.is_future_date(event_report_date_str):
            buttons.append([InlineKeyboardButton("Event Report", callback_data=f"EVENT-event_report-{event_id}")])

        if await time.is_future_date(proposal_form_date_str):
            buttons.append([InlineKeyboardButton("Proposal Form", callback_data=f"EVENT-proposal_form-{event_id}")])

        if await time.is_future_date(flyer_and_schedule_date_str):
            buttons.append([InlineKeyboardButton("Flyer and Schedule", callback_data=f"EVENT-flyer_and_schedule-{event_id}")])

        if await time.is_future_date(list_of_participants_date_str):
            buttons.append([InlineKeyboardButton("List of Participants", callback_data=f"EVENT-list_of_participants-{event_id}")])

        # Always add Edit and Delete buttons if the event date is not exceeded
        buttons.append([InlineKeyboardButton("Add Reporter Details",callback_data=f"EVENT-add_reporter_details-{event_id}")])
        if chat_id in council_chat_ids:
            buttons.append([InlineKeyboardButton("Edit", callback_data=f"EVENT-edit_event_info-{event_id}")])
            buttons.append([InlineKeyboardButton("Delete", callback_data=f"EVENT-delete_event_info-{event_id}-{event_name}")])  # Assuming 'reporter_name' is used
        buttons.append(await generate_club_event_buttons(club_id=club_id,back_button_to_view=True))
    else:
        print(f"No event found with ID {event_id}. Buttons will not be generated.")

    return buttons  # Return the button list (can be empty if the date has passed)
# async def generate_datetime_buttons():
#     # Generate Year Buttons (example from 2020 to 2025)
#     years = [[InlineKeyboardButton(str(year), callback_data=f"year:{year}") for year in range(2020, 2026)]]

#     # Generate Month Buttons (1 to 12)
#     months = [[InlineKeyboardButton(str(month).zfill(2), callback_data=f"month:{month}") for month in range(1, 13)]]

#     # Generate Day Buttons (1 to 31)
#     days = [[InlineKeyboardButton(str(day).zfill(2), callback_data=f"day:{day}") for day in range(1, 32)]]

#     # Generate Hour Buttons (00 to 23)
#     hours = [[InlineKeyboardButton(str(hour).zfill(2), callback_data=f"hour:{hour}") for hour in range(0, 24)]]

#     # Generate Minute and Second Buttons (00 to 59)
#     minutes = [[InlineKeyboardButton(str(minute).zfill(2), callback_data=f"minute:{minute}") for minute in range(0, 60, 5)]]
#     seconds = [[InlineKeyboardButton(str(second).zfill(2), callback_data=f"second:{second}") for second in range(0, 60, 10)]]

#     # Combine all into one inline keyboard
#     keyboard = years + months + days + hours + minutes + seconds

#     return InlineKeyboardMarkup(keyboard)


async def get_all_events_buttons():
    # Retrieve all event IDs and names
    event_data = await sqlitedb.get_event_ids_and_names()
    
    # Check if there are any events
    if not event_data:
        return False,"There are no active events",InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")]])  # Return False if no events are found

    # Initialize the keyboard markup for inline buttons
    buttons = []

    # Loop through each event and create a button
    for event_id, event_name in event_data:
        # Create an InlineKeyboardButton for each event
        # club_id = await sqlitedb.get_club_id_by_event_id(event_id=event_id)
        button = InlineKeyboardButton(
            text=event_name,  # Button text is the event name
            callback_data=f"EVENT-view_event_details-{event_id}"  # Callback data with event_id
        )
        # Add each button as a list item to the buttons array
        buttons.append([button])
    buttons.append([InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")])
    # Create the inline keyboard layout
    keyboard = InlineKeyboardMarkup(buttons)
    
    # Return True for status and the inline keyboard
    return True,"Click on event to get more details", keyboard

async def generate_date_picker_buttons(method,current_day, current_month, current_year):
    # Create buttons for the "Up" arrows
    up_buttons = [
        InlineKeyboardButton("⬆️", callback_data=f"{method}-date-day-up-{current_day}-{current_month}-{current_year}"),
        InlineKeyboardButton("⬆️", callback_data=f"{method}-date-month-up-{current_day}-{current_month}-{current_year}"),
        InlineKeyboardButton("⬆️", callback_data=f"{method}-date-year-up-{current_day}-{current_month}-{current_year}")
    ]
    
    # Create buttons to display the current day, month, and year
    date_buttons = [
        InlineKeyboardButton(str(current_day).zfill(2), callback_data=f"{method}-day-{current_day}"),
        InlineKeyboardButton(str(current_month).zfill(2), callback_data=f"{method}-month-{current_month}"),
        InlineKeyboardButton(str(current_year), callback_data=f"{method}-year-{current_year}")
    ]
    
    # Create buttons for the "Down" arrows
    down_buttons = [
        InlineKeyboardButton("⬇️", callback_data=f"{method}-date-day-down-{current_day}-{current_month}-{current_year}"),
        InlineKeyboardButton("⬇️", callback_data=f"{method}-date-month-down-{current_day}-{current_month}-{current_year}"),
        InlineKeyboardButton("⬇️", callback_data=f"{method}-date-year-down-{current_day}-{current_month}-{current_year}")
    ]
    submit_button = [
        InlineKeyboardButton("Submit",callback_data=f"{method}-submit-date-{current_day}-{current_month}-{current_year}")
    ]
    # Combine the rows into an inline keyboard
    keyboard = [up_buttons, date_buttons, down_buttons, submit_button]
    
    return InlineKeyboardMarkup(keyboard)

async def generate_time_picker_buttons(method, current_hour, current_minute, period):
    # Create buttons for the "Up" arrows
    up_buttons = [
        InlineKeyboardButton("⬆️", callback_data=f"{method}-time-hour-up-{current_hour}-{current_minute}-{period}"),
        InlineKeyboardButton("⬆️", callback_data=f"{method}-time-minute-up-{current_hour}-{current_minute}-{period}"),
        InlineKeyboardButton("⬆️", callback_data=f"{method}-time-period-up-{current_hour}-{current_minute}-{period}")
    ]
    
    # Create buttons to display the current hour, minute, and period (AM/PM)
    time_buttons = [
        InlineKeyboardButton(str(current_hour).zfill(2), callback_data=f"{method}-hour-{current_hour}"),
        InlineKeyboardButton(str(current_minute).zfill(2), callback_data=f"{method}-minute-{current_minute}"),
        InlineKeyboardButton(period, callback_data=f"{method}-period-{period}")
    ]
    
    # Create buttons for the "Down" arrows
    down_buttons = [
        InlineKeyboardButton("⬇️", callback_data=f"{method}-time-hour-down-{current_hour}-{current_minute}-{period}"),
        InlineKeyboardButton("⬇️", callback_data=f"{method}-time-minute-down-{current_hour}-{current_minute}-{period}"),
        InlineKeyboardButton("⬇️", callback_data=f"{method}-time-period-down-{current_hour}-{current_minute}-{period}")
    ]
    submit_button = [
        InlineKeyboardButton("Submit", callback_data=f"{method}-submit-time-{current_hour}-{current_minute}-{period}")
    ]
    
    # Combine the rows into an inline keyboard
    keyboard = [up_buttons, time_buttons, down_buttons, submit_button]
    
    return InlineKeyboardMarkup(keyboard)

async def edit_clubs_info_buttons(club_id):
    """
    Generate buttons for editing club information.
    
    :param club_id: The ID of the club.
    :param club_name: The name of the club.
    :param club_description: The description of the club.
    :param club_president: The president of the club.
    :param club_vice_president: The vice president of the club.
    :returns: InlineKeyboardMarkup object with edit buttons.
    """
    # Create the inline keyboard markup
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Name", callback_data=f"CLUB-edit_club_info_selected-{club_id}-name")],
            [InlineKeyboardButton("Description", callback_data=f"CLUB-edit_club_info_selected-{club_id}-description")],
            [InlineKeyboardButton("President", callback_data=f"CLUB-edit_club_info_selected-{club_id}-president")],
            [InlineKeyboardButton("Vice President", callback_data=f"CLUB-edit_club_info_selected-{club_id}-vice_president")],
            [InlineKeyboardButton("Back",callback_data = "CLUB-back_to_clubs")]
        ]
        )
    
    return keyboard
    

async def edit_event_info_buttons(event_id: int):
    """
    Generate buttons for editing event information.
    
    :param event_id: The ID of the event.
    :return: InlineKeyboardMarkup object with edit buttons.
    """
    club_id = await sqlitedb.get_club_id_by_event_id(event_id=event_id)
    # Create the inline keyboard markup
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Name", callback_data=f"EVENT-edit_event_info_selected-{event_id}-name")],
            [InlineKeyboardButton("Number of Days", callback_data=f"EVENT-edit_event_info_selected-{event_id}-number_of_days")],
            [InlineKeyboardButton("Date and Time", callback_data=f"EVENT-edit_event_info_selected-{event_id}-date_time")],
            [InlineKeyboardButton("Venue", callback_data=f"EVENT-edit_event_info_selected-{event_id}-venue")],
            [InlineKeyboardButton("Audience Size", callback_data=f"EVENT-edit_event_info_selected-{event_id}-audience_size")],
            [InlineKeyboardButton("Type", callback_data=f"EVENT-edit_event_info_selected-{event_id}-type")],
            [InlineKeyboardButton("Back", callback_data=f"EVENT-view_events-{club_id}")]
        ]
    )
    
    return keyboard
async def clubs_buttons():
    """
    This function is used to generate the clubs buttons.
    :returns: A tuple with a boolean and the button value (or an empty string).
    """
    # Fetch club names and their IDs from the database
    club_names_ids = await sqlitedb.get_club_names_and_indexes()

    # Initialize the list of buttons
    Button = []
    
    # Check if there is at least one club
    if len(club_names_ids) >= 1:
        for club_id, club_name in club_names_ids:
            Button.append([InlineKeyboardButton(f"{club_name}", callback_data=f"CLUB-club_detailed_view|edit-{club_name}-{club_id}")])
        Button.append(back_to_initial_clubs_button)
        # Create the final keyboard markup
        Final_Button = InlineKeyboardMarkup(inline_keyboard=Button)
        
        # Return True and the final button markup
        return True, Final_Button
    else:
        # Return False and an empty string if there are no clubs
        return False, ''

async def event_buttons(chat_id=None,club_id=None):
    """
    This function generates the event buttons.
    :returns: A tuple with a boolean and the button value (or an empty string).
    """
    if chat_id is not None:
        if chat_id in await sqlitedb.get_pres_and_vice_pres_chat_ids():
            club_id = await sqlitedb.get_club_id_by_chat_id(chat_id=chat_id)
            event_ids_and_names = await sqlitedb.get_event_ids_and_names_by_club_id(club_id=club_id)
            buttons = []
            if len(event_ids_and_names) >= 1:
                for event_id, event_name in event_names_ids:
                    buttons.append([InlineKeyboardButton(f"{event_name}", callback_data=f"EVENT-event_detailed_view|edit-{event_id}")])
                buttons.append([InlineKeyboardButton("Back", callback_data=f"EVENT-back_to_events_menu-{club_id}")])
                final_buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
                return True, final_buttons
            else:
                # Return False and an empty string if there are no events
                return False, ''
    elif club_id is not None:
            event_ids_and_names = await sqlitedb.get_event_ids_and_names_by_club_id(club_id=club_id)
            buttons = []
            if len(event_ids_and_names) >= 1:
                for event_id, event_name in event_ids_and_names:
                    buttons.append([InlineKeyboardButton(f"{event_name}", callback_data=f"EVENT-event_detailed_view|edit-{event_id}")])
                buttons.append([InlineKeyboardButton("Back", callback_data=f"EVENT-back_to_events_menu-{club_id}")])
                final_buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
                return True, final_buttons
            else:
                # Return False and an empty string if there are no events
                return False, ''
    else:
        # Fetch event names and their IDs from the database
        event_names_ids = await sqlitedb.get_event_ids_and_names()
        # Initialize the list of buttons
        buttons = []
        # Check if there is at least one event
        if len(event_names_ids) >= 1:
            for event_id, event_name in event_names_ids:
                buttons.append([InlineKeyboardButton(f"{event_name}", callback_data=f"EVENT-event_detailed_view|edit-{event_id}")])
            buttons.append([InlineKeyboardButton("Back", callback_data=f"EVENT-back_to_events_menu-{club_id}")])
            # Create the final keyboard markup
            final_buttons = InlineKeyboardMarkup(inline_keyboard=buttons)

            # Return True and the final button markup
            return True, final_buttons
        else:
            # Return False and an empty string if there are no events
            return False, ''


async def event_clubs_buttons():
    """
    This function is used to generate the clubs buttons when viewed from event point of view.
    :returns: A tuple with a boolean and the button value (or an empty string).
    """
    # Fetch club names and their IDs from the database
    club_names_ids = await sqlitedb.get_club_names_and_indexes()

    # Initialize the list of buttons
    Button = []
    
    # Check if there is at least one club
    if len(club_names_ids) >= 1:
        for club_id, club_name in club_names_ids:
            Button.append([InlineKeyboardButton(f"{club_name}", callback_data=f"EVENT-club_event-{club_name}-{club_id}")])
        Button.append(back_to_initial_clubs_button)
        # Create the final keyboard markup
        Final_Button = InlineKeyboardMarkup(inline_keyboard=Button)
        
        # Return True and the final button markup
        return True, Final_Button
    else:
        # Return False and an empty string if there are no clubs
        return False, ''

async def clubs_callback_function(bot,callback_query):
    """
    This Function performs operations based on the callback data from the user for the clubs.
    :param bot: Client session.
    :param callback_query: callback data of the user.

    :return: This returns nothing, But performs operations.
    """
    # if "club_event" in callback_query.data:
    #     club_name = callback_query.data.split("-")[1]
    #     club_id = callback_query.data.split("-")[2]
    #     await callback_query.edit_message_text(
    #         club_events_templates.ADD_EVENTS[0],
    #         reply_markup = add_view_events_button
    #     )
    if callback_query.data == "CLUB-back_to_clubs":
        await callback_query.answer()

        # Get the buttons and the boolean value from the clubs_buttons function
        buttons_available, buttons_markup = await clubs_buttons()

        if buttons_available:
            # If buttons are available, use the markup
            await callback_query.edit_message_text(
                club_events_templates.CLUB_NAMES_TEXT,
                reply_markup=buttons_markup
            )
        else:
            # If no buttons are available, provide an appropriate response
            button = InlineKeyboardMarkup(inline_keyboard=[(back_to_initial_clubs_button)])
            NO_CLUBS_AVAILABLE = "There are no clubs available"
            await callback_query.edit_message_text(
                NO_CLUBS_AVAILABLE,
                reply_markup = button
            )
    elif callback_query.data == "CLUB-add_club":
        chat_id = callback_query.message.chat.id
        await callback_query.message.delete()
        await sqlitedb.set_permissions(chat_id,clubs=True)
        await club_event_service.add_club_details(bot,chat_id)
    elif callback_query.data == "CLUB-view_clubs":
        await callback_query.answer()
        # Get the buttons and the boolean value from the clubs_buttons function
        buttons_available, buttons_markup = await clubs_buttons()

        if buttons_available:
            # If buttons are available, use the markup
            await callback_query.edit_message_text(
                club_events_templates.CLUB_NAMES_TEXT,
                reply_markup=buttons_markup
            )
        else:
            # If no buttons are available, provide an appropriate response
            button = InlineKeyboardMarkup(inline_keyboard=[(back_to_initial_clubs_button)])
            NO_CLUBS_AVAILABLE = "There are no clubs available"
            await callback_query.edit_message_text(
                NO_CLUBS_AVAILABLE,
                reply_markup = button
            )
    elif callback_query.data.split("-")[1] == "club_member_dashboard":
        chat_id = callback_query.message.chat.id
        club_info  = await sqlitedb.get_club_info_by_chat_id(chat_id=chat_id)
        club_id = club_info['id']
        club_name = club_info["name"]
        text = await council_templates.generate_club_info_text_single_message(club_info)
        buttons = []
        buttons.append(InlineKeyboardButton("EVENTS",callback_data=f"EVENT-club_event-{club_name}-{club_id}"))
        buttons = InlineKeyboardMarkup(inline_keyboard=[buttons])
        await callback_query.edit_message_text(
            text,
            reply_markup = buttons
        )
    elif callback_query.data.split("-")[1] == "club_detailed_view|edit":
        club_name = callback_query.data.split("-")[2]
        club_id = callback_query.data.split("-")[3]
        chat_id = callback_query.message.chat.id
        await sqlitedb.set_permissions(chat_id, clubs=False)
        club_info = await sqlitedb.get_club_info_by_id(int(club_id))
        # print(club_info)
        # if len(club_info) == 5:
        stored_club_id,club_name,club_description,club_president,club_president_chat_id,club_vice_president,club_vc_pres_chat_id = club_info
        club_info_text = f"""
```CLUB INFO

CLUB NAME : {club_name}
CLUB DESCRIPTION : {club_description}
PRESIDENT : {club_president}
VICE PRESIDENT : {club_vice_president}
```
"""
        button = []
        button.append([InlineKeyboardButton("Edit",callback_data=f"CLUB-edit_club_info-{club_id}")])
        button.append([InlineKeyboardButton("Events",callback_data=f"EVENT-back_to_events_menu-{club_id}")])
        button.append([InlineKeyboardButton("Delete",callback_data=f"CLUB-delete_club_info-{club_id}-{club_name}")])
        button.append(back_to_clubs_button)
        button = InlineKeyboardMarkup(
            inline_keyboard=button
        )
        await callback_query.edit_message_text(
            club_info_text,
            reply_markup = button
        )
    elif callback_query.data.split("-")[1] == "delete_club_info":
        club_id = callback_query.data.split("-")[2]
        await sqlitedb.delete_club_by_id(int(club_id))
        club_name = callback_query.data.split("-")[3]
        # Add postgres version to delete from main database
        Deletion_text = f"Successfully Deleted Club {club_name}"
        button = []
        button.append(back_to_clubs_button)
        button = InlineKeyboardMarkup(inline_keyboard=button)
        await callback_query.edit_message_text(
            Deletion_text,
            reply_markup = button
        )
    elif callback_query.data == "CLUB-back_to_initial_clubs":
        await callback_query.answer()
        await callback_query.edit_message_text(
            club_events_templates.ADD_CLUBS[0],
            reply_markup = add_view_clubs_button
        )
    elif callback_query.data.split("-")[1] == "edit_club_info":
        club_id = callback_query.data.split("-")[2]
        club_info = await sqlitedb.get_club_info_by_id(int(club_id))
        stored_club_id,club_name,club_description,club_president,club_president_chat_id,club_vice_president,club_vc_pres_chat_id = club_info
        club_info_text = f"""
```CLUB INFO

CLUB NAME : {club_name}
CLUB DESCRIPTION : {club_description}
PRESIDENT : {club_president}
VICE PRESIDENT : {club_vice_president}

WHAT YOU WOULD LIKE TO EDIT.
```
"""
        button = await edit_clubs_info_buttons(club_id=int(club_id))
        await callback_query.edit_message_text(
            club_info_text,
            reply_markup = button
        )
    elif callback_query.data.split("-")[1] == "edit_club_info_selected":
        chat_id = callback_query.message.chat.id
        club_id = int(callback_query.data.split("-")[2])
        club_action = callback_query.data.split("-")[3]

        # Set permissions for the chat
        await sqlitedb.set_permissions(chat_id, edit_clubs=club_action)
            # Fetch the current club information
        club_info = await sqlitedb.get_club_info_by_id(club_id)
        print(club_info)
        if len(club_info) == 7:
            stored_club_id, club_name, club_description, club_president,pres_chat_id, club_vice_president,vice_pres_chat_id = club_info
            print(stored_club_id)
        if club_action == "name":
                # Store the current club information temporarily
                await sqlitedb.store_temp_club_info(
                    chat_id,club_id=stored_club_id,
                    description=club_description,
                    president=club_president,
                    vice_president=club_vice_president
                )

        elif club_action == "description":
                # Store the current club information temporarily
                await sqlitedb.store_temp_club_info(
                    chat_id,club_id=stored_club_id,
                    name=club_name,
                    president=club_president,
                    vice_president=club_vice_president
                )

        elif club_action == "president":
                # Store the current club information temporarily
                await sqlitedb.store_temp_club_info(
                    chat_id,club_id=stored_club_id,
                    name=club_name,
                    description=club_description,
                    vice_president=club_vice_president,
                    vice_pres_chat_id = vice_pres_chat_id
                )

        elif club_action == "vice_president":
                # Store the current club information temporarily
                await sqlitedb.store_temp_club_info(
                    chat_id,club_id=stored_club_id,
                    name=club_name,
                    description=club_description,
                    president=club_president,
                    pres_chat_id=pres_chat_id
                )
        # Call the service to handle the next steps
        await club_event_service.add_club_details(bot, chat_id)




async def events_callback_function(bot,callback_query):
    """
    This Function performs operations based on the callback data from the user for the events.
    :param bot: Client session.
    :param callback_query: callback data of the user.

    :return: This returns nothing, But performs operations.
    """
    data_part = callback_query.data.split("-")
    print(data_part)
    # print(data_part)
    if data_part[1] == "club_event":
        chat_id = callback_query.message.chat.id
        await callback_query.answer()
        # Get the buttons and the boolean value from the clubs_buttons function
        buttons_available, buttons_markup = await event_clubs_buttons()
        council_admins_chat_id = await sqlitedb.get_all_student_council_chat_ids()
        clubs_pres_vc_pres_chat_ids = await sqlitedb.get_pres_and_vice_pres_chat_ids()
        if buttons_available:
            if chat_id in council_admins_chat_id:
            # If buttons are available, use the markup
                await callback_query.edit_message_text(
                    club_events_templates.CLUB_NAMES_TEXT,
                    reply_markup=buttons_markup
                )
            elif chat_id in clubs_pres_vc_pres_chat_ids:
                club_info = await sqlitedb.get_club_info_by_chat_id(chat_id)
                # print(club_info)
                club_id = club_info['id']
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[0],
                    reply_markup = await generate_club_event_buttons(club_id=club_id,chat_id=chat_id)
                )
        else:
            # If no buttons are available, provide an appropriate response
            button = InlineKeyboardMarkup(inline_keyboard=[(back_to_initial_clubs_button)])
            NO_CLUBS_AVAILABLE = "There are no clubs available"
            await callback_query.edit_message_text(
                NO_CLUBS_AVAILABLE,
                reply_markup = button
            )
        # [InlineKeyboardButton("Add Event", callback_data="EVENT-add_event")],
        # [InlineKeyboardButton("View Events", callback_data="EVENT-view_events")]
    elif data_part[1] == "event_report":
        chat_id = callback_query.message.chat.id
        event_id = data_part[2]
        # print(data_part)
        # print(event_id)
        print(f"Data part : {data_part} , Event id : {event_id}")
        await sqlitedb.set_permissions(chat_id=chat_id,report_upload=f"{event_id}")
        await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[0])
    elif data_part[1] == "proposal_form":
        chat_id = callback_query.message.chat.id
        event_id = data_part[2]
        # print(data_part)
        # print(event_id)
        print(f"Data part : {data_part} , Event id : {event_id}")
        await sqlitedb.set_permissions(chat_id=chat_id,proposal_form=f"{event_id}")
        print(await sqlitedb.check_permission(chat_id=chat_id,proposal_form=True))
        await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[1])
    elif data_part[1] == "flyer_and_schedule":
        chat_id = callback_query.message.chat.id
        event_id = data_part[2]
        # print(data_part)
        # print(event_id)
        print(f"Data part : {data_part} , Event id : {event_id}")
        await sqlitedb.set_permissions(chat_id=chat_id,flyer=f"{event_id}")
        await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[2])
    elif data_part[1] == "list_of_participants":
        chat_id = callback_query.message.chat.id
        event_id = data_part[2]
        # print(data_part)
        # print(event_id)
        print(f"Data part : {data_part} , Event id : {event_id}")
        await sqlitedb.set_permissions(chat_id=chat_id,list_of_participants=f"{event_id}")
        await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[3])
    elif data_part[1] == "add_reporter_details":
        chat_id = callback_query.message.chat.id
        event_id = data_part[2]
        # print(data_part)
        print(f"Data part : {data_part} , Event id : {event_id}")
        await sqlitedb.set_permissions(chat_id=chat_id,reporter_details=f"{event_id}")
        await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[6])
    elif data_part[1] == "view_event_details":
        event_id = data_part[2]
        event_details = await sqlitedb.get_event_info_by_id(event_id=event_id)
        id, name, number_of_days, date_time, venue, audience_size, type,club_id = event_details
        club_name = await sqlitedb.get_club_name_by_club_id(club_id=club_id)
        event_details_text = f"""
```EVENT DETAILS

Name : {name}
Number of days : {number_of_days}
date and time : {date_time}
venue : {venue}
audience size : {audience_size}
type : {type}
club name : {club_name}
```
"""
        back_button  = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Back",callback_data=f"EVENT-all_events")]])
        await callback_query.edit_message_text(
            event_details_text,
            reply_markup = back_button
        )

    elif data_part[1] == "add_event":
        chat_id = callback_query.message.chat.id
        club_id = data_part[2]
        chat_id = callback_query.message.chat.id
        await callback_query.message.delete()
        await sqlitedb.set_permissions(chat_id,events=True)
        await club_event_service.add_event_details(bot,chat_id)
        await sqlitedb.store_temp_event_info(chat_id=chat_id,club_id=club_id)
    elif data_part[1] == "view_events":
        club_id = data_part[2]
        chat_id = callback_query.message.chat.id
        await callback_query.answer()
        council_admins_chat_id = await sqlitedb.get_all_student_council_chat_ids()
        clubs_pres_vc_pres_chat_ids = await sqlitedb.get_pres_and_vice_pres_chat_ids()

        buttons_available = False
        buttons_markup = None
        if club_id:
            buttons_available,buttons_markup = await event_buttons(club_id=club_id)
        elif chat_id in council_admins_chat_id:
            # Get the buttons and the boolean value from the clubs_buttons function
            buttons_available, buttons_markup = await event_buttons()

        elif chat_id in clubs_pres_vc_pres_chat_ids:
            buttons_available, buttons_markup = await event_buttons(chat_id=chat_id)
        
        if buttons_available:
                # If buttons are available, use the markup
                await callback_query.edit_message_text(
                    club_events_templates.EVENT_NAMES_TEXT,
                    reply_markup=buttons_markup
                )
        else:
            # If no buttons are available, provide an appropriate response
            button = InlineKeyboardMarkup(inline_keyboard=[([InlineKeyboardButton("Back", callback_data=f"EVENT-back_to_events_menu-{club_id}")])])
            NO_EVENTS_AVAILABLE = "There are no events available"
            await callback_query.edit_message_text(
                NO_EVENTS_AVAILABLE,
                reply_markup = button
            )
    elif data_part[1] == "event_detailed_view|edit":
        # EVENT-event_detailed_view|edit-{event_name}-{event_id}
        # event_name = data_part[2]
        event_id = data_part[2]
        chat_id = callback_query.message.chat.id
        await sqlitedb.set_permissions(chat_id, events=False)
        event_info = await sqlitedb.get_event_info_by_id(event_id=event_id)
        event_id,event_name,number_of_days,date_time,venue,audience_size,type_of_event,_ = event_info
        event_date = date_time.split("-")[0]
        # event_date = event_date.replace(":","/")
        event_time = date_time.split("-")[1]
        event_info_text = f"""
```EVENT INFO

EVENT NAME : {event_name}
NO OF DAYS : {number_of_days}
DATE : {event_date}
TIME : {event_time}
VENUE : {venue}
AUDIENCE SIZE : {audience_size}
TYPE OF EVENT : {type_of_event}
```
"""
        # button = []
        # button.append([InlineKeyboardButton("Edit",callback_data=f"EVENT-edit_event_info-{event_id}")])
        # button.append([InlineKeyboardButton("Delete",callback_data=f"EVENT-delete_event_info-{event_id}-{event_name}")])
        # button.append(back_to_events_button)
        button = InlineKeyboardMarkup(
            inline_keyboard=await generate_event_altering_receiving_buttons(event_id=event_id,event_name=event_name)
        )
        await callback_query.edit_message_text(
            event_info_text,
            reply_markup = button
        )
    elif data_part[1] == "back_to_events_menu":
        await callback_query.answer()
        # print(data_part)
        chat_id = callback_query.message.chat.id
        club_id = data_part[2]
        await callback_query.edit_message_text(
            club_events_templates.ADD_EVENTS[0],
            reply_markup = await generate_club_event_buttons(club_id=club_id,back_button_to_view=False,chat_id=chat_id)
        )
    elif data_part[1] == "all_events":
        status,text,keyboard = await get_all_events_buttons()
        await callback_query.edit_message_text(
            text,
            reply_markup = keyboard
        )
    elif data_part[1] == "edit_event_info":
        chat_id = callback_query.message.chat.id
        event_id = data_part[2]
        event_info = await sqlitedb.get_event_info_by_id(event_id)
        await sqlitedb.set_permissions(chat_id)
        _,event_name,number_of_days,date_time,venue,audience_size,type_of_event,_ = event_info
        event_date = date_time.split("-")[0]
        event_time = date_time.split("-")[1]
        event_info_text = f"""
```EVENT INFO

EVENT NAME : {event_name}
NO OF DAYS : {number_of_days}
DATE : {event_date}
TIME : {event_time}
VENUE : {venue}
AUDIENCE SIZE : {audience_size}
TYPE OF EVENT : {type_of_event}

WHAT YOU WOULD LIKE TO EDIT.
```
"""
        button = []
        button = await edit_event_info_buttons(event_id)
        await callback_query.edit_message_text(
            event_info_text,
            reply_markup = button
        )

    elif callback_query.data.split("-")[1] == "delete_event_info":
        event_id = callback_query.data.split("-")[2]
        await sqlitedb.delete_event_by_id(int(event_id))
        event_name = callback_query.data.split("-")[3]
        # Add postgres version to delete from main database
        Deletion_text = f"Successfully Deleted event {event_name}"
        button = []
        button.append(await generate_club_event_buttons(back_button_to_view=True))
        button = InlineKeyboardMarkup(inline_keyboard=button)
        await callback_query.edit_message_text(
            Deletion_text,
            reply_markup = button
        )
                # [InlineKeyboardButton("Name", callback_data=f"EVENT-edit_event_info_selected-{event_id}-name")],
    elif data_part[1] == "edit_event_info_selected":
        chat_id = callback_query.message.chat.id
        event_id = int(callback_query.data.split("-")[2])
        event_edit_action = callback_query.data.split("-")[3]

        # Set permission for the chat
        await sqlitedb.set_permissions(chat_id=chat_id, edit_events=event_edit_action)
        await sqlitedb.delete_temp_event_by_chat_id(chat_id)
        # Fetch the current event information
        event_info = await sqlitedb.get_event_info_by_id(event_id)

        if len(event_info) == 7:
            stored_event_id, event_name, event_no_of_days, event_date_time, event_venue, event_audience_size, event_type , _= event_info

        if event_edit_action == "name":
            # Store event info temporarily
            await sqlitedb.store_temp_event_info(
                chat_id=chat_id,
                event_id=stored_event_id,
                number_of_days=event_no_of_days,
                date_time=event_date_time,
                venue=event_venue,
                audience_size=event_audience_size,
                type=event_type
            )
            await callback_query.answer()
        elif event_edit_action == "number_of_days":
            # Store the current event information temporarily
            await sqlitedb.store_temp_event_info(
                chat_id=chat_id,
                event_id=stored_event_id,
                name=event_name,
                date_time=event_date_time,
                venue=event_venue,
                audience_size=event_audience_size,
                type=event_type
            )
            await callback_query.answer()
        elif event_edit_action == "date_time":
            # Store the current event information temporarily
            await sqlitedb.store_temp_event_info(
                chat_id=chat_id,
                event_id=stored_event_id,
                name=event_name,
                number_of_days=event_no_of_days,
                venue=event_venue,
                audience_size=event_audience_size,
                type=event_type
            )
            current_date = await time.get_current_date()
            current_day = current_date.day
            current_month = current_date.month
            current_year = current_date.year
            await bot.send_message(chat_id,club_events_templates.ADD_EVENTS[1],reply_markup = await generate_date_picker_buttons(method="EVENT-edit",current_day=current_day,current_month=current_month,current_year=current_year))

        elif event_edit_action == "venue":
            # Store the current event information temporarily
            await sqlitedb.store_temp_event_info(
                chat_id=chat_id,
                event_id=stored_event_id,
                name=event_name,
                number_of_days=event_no_of_days,
                date_time=event_date_time,
                audience_size=event_audience_size,
                type=event_type
            )
            await callback_query.answer()

        elif event_edit_action == "audience_size":
            # Store the current event information temporarily
            await sqlitedb.store_temp_event_info(
                chat_id=chat_id,
                event_id=stored_event_id,
                name=event_name,
                number_of_days=event_no_of_days,
                date_time=event_date_time,
                venue=event_venue,
                type=event_type
            )
            await callback_query.answer()

        elif event_edit_action == "type":
            # Store the current event information temporarily
            await sqlitedb.store_temp_event_info(
                chat_id=chat_id,
                event_id=stored_event_id,
                name=event_name,
                number_of_days=event_no_of_days,
                date_time=event_date_time,
                venue=event_venue,
                audience_size=event_audience_size
            )
            await bot.send_message(chat_id,club_events_templates.ADD_EVENTS[2],reply_markup = await generate_time_picker_buttons(method="EVENT-edit",current_hour=12,current_minute=00,current_period = "AM"))
        # Call the service to handle the next steps
        await club_event_service.add_event_details(bot, chat_id)
    elif data_part[1] == "edit":
        edit_action_part = data_part[2]#date or time-hour-up-{current_hour}-{current_minute}-{period}
        action_applied = data_part[4] # Up or down
                # InlineKeyboardButton("⬇️", callback_data=f"{method}-date-day-down-{current_day}-{current_month}-{current_year}"),
        if action_applied == "up":
            if edit_action_part == "date":
                current_day = int(callback_query.data.split("-")[5])
                current_month = int(callback_query.data.split("-")[6])
                current_year = int(callback_query.data.split("-")[7])

                if data_part[3] == "day":
                    current_day += 1
                elif data_part[3] == "month":
                    current_month += 1
                elif data_part[3] == "year":
                    current_year += 1
                else:
                    return

                if current_month > 12:
                    current_month = 1
                    current_year += 1

                days_in_month = calendar.monthrange(current_year, current_month)[1]

                if current_day > days_in_month:
                    current_day = 1
                    current_month += 1
                    if current_month > 12:
                        current_month = 1
                        current_year += 1

                try:
                    await callback_query.edit_message_text(
                        club_events_templates.ADD_EVENTS[1],
                        reply_markup=await generate_date_picker_buttons(
                            method="EVENT-edit",
                            current_day=current_day,
                            current_month=current_month,
                            current_year=current_year
                        )
                    )
                except:
                    print("")
                
            elif data_part[1] == "time":
                current_hour = int(callback_query.data.split("-")[5])
                current_minute = int(callback_query.data.split("-")[6])
                current_period = callback_query.data.split("-")[7]

                if data_part[3] == "hour":
                    current_hour += 1
                elif data_part[3] == "minute":
                    current_minute += 5
                elif data_part[3] == "period":
                    current_period = "PM" if current_period == "AM" else "AM"
                else:
                    return

                if current_hour > 12:
                    current_hour = 1
                    current_period = "PM" if current_period == "AM" else "AM"

                if current_minute >= 60:
                    current_minute = 0
                    current_hour += 1
                    if current_hour > 12:
                        current_hour = 1
                        current_period = "PM" if current_period == "AM" else "AM"

                try:
                    await callback_query.edit_message_text(
                        club_events_templates.ADD_EVENTS[2],
                        reply_markup=await generate_time_picker_buttons(
                            method="EVENT-edit",
                            current_hour=current_hour,
                            current_minute=current_minute,
                            period=current_period
                        )
                    )
                except:
                    print("")
        elif action_applied == "down":
            if data_part[1] == "date":
                current_day = int(data_part[5])
                current_month = int(data_part[6])
                current_year = int(data_part[7])

                if data_part[3] == "day":
                    current_day -= 1
                elif data_part[3] == "month":
                    current_month -= 1
                elif data_part[3] == "year":
                    current_year -= 1
                else:
                    return

                if current_month < 1:
                    current_month = 12
                    current_year -= 1

                days_in_month = calendar.monthrange(current_year, current_month)[1]

                if current_day < 1:
                    current_month -= 1
                    if current_month < 1:
                        current_month = 12
                        current_year -= 1
                    days_in_month = calendar.monthrange(current_year, current_month)[1]
                    current_day = days_in_month
                try:
                    await callback_query.edit_message_text(
                        club_events_templates.ADD_EVENTS[1],
                        reply_markup=await generate_date_picker_buttons(
                            method="EVENT-edit",
                            current_day=current_day,
                            current_month=current_month,
                            current_year=current_year
                        )
                    )
                except Exception as e:
                    print(f"{e}")
            elif action_applied == "time":
                current_hour = int(data_part[5])
                current_minute = int(data_part[6])
                current_period = data_part[7]
                if data_part[3] == "hour":
                    current_hour -= 1
                elif data_part[3] == "minute":
                    current_minute -= 5
                elif data_part[3] == "period":
                    current_period = "AM" if current_period == "PM" else "PM"
                else:
                    return
                if current_hour < 1:
                    current_hour = 12
                if current_minute < 0:
                    current_minute = 55
                    current_hour -= 1
                    if current_hour < 1:
                        current_hour = 12
                        current_period = "AM" if current_period == "PM" else "PM"
                try:
                    await callback_query.edit_message_text(
                        club_events_templates.ADD_EVENTS[2],
                        reply_markup=await generate_time_picker_buttons(
                            method="EVENT-edit",
                            current_hour=current_hour,
                            current_minute=current_minute,
                            period=current_period
                        )
                    )
                except Exception as e:
                    print(f"{e}")
                    # "Submit",callback_data=f"{method}-submit-date-{current_day}-{current_month}-{current_year}")
        elif edit_action_part == "submit":
            chat_id = callback_query.message.chat.id
            if data_part[3] == "date":
                current_day = data_part[4]
                current_month = data_part[5]
                current_year = data_part[6]
                try:
                    await sqlitedb.store_temp_event_info(chat_id,date_time=f"{current_day}/{current_month}/{current_year}") #DD/MM/YYYY
                    await callback_query.edit_message_text(
                        club_events_templates.ADD_EVENTS[2],
                        reply_markup = await generate_time_picker_buttons(method="EVENT-edit",current_hour=12, current_minute=00,period="AM")
                    )
                except Exception as e:
                    print(f"Error : {e}")
            elif data_part[3] == "time":
                current_hour = data_part[4]
                current_minute = data_part[5]
                if int(current_minute) < 10:
                    current_minute = f"0{current_minute}"
                if int(current_hour) < 10:
                    current_hour = f"0{current_hour}"
                current_period = data_part[5]
                data = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id) #(1767667538, None, 'hell', 1, '17/12/2024', 'iare', 1, None)
                date = data[4]
                date_time = date + f"-{current_hour}:{current_minute}:{current_period}"
                await sqlitedb.store_temp_event_info(chat_id = chat_id,date_time=date_time)
                await club_event_handler.store_edited_event_values(chat_id)
                await sqlitedb.set_permissions(chat_id)
                temp_event_info = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id=chat_id)
                event_id = temp_event_info[0]
                button = []
                button.append([InlineKeyboardButton("Back",callback_data=f"EVENT-edit_event_info-{event_id}")])
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[5],
                    reply_markup = button
                )
            elif data_part[1] == "tech_event":
                chat_id = callback_query.message.chat.id
                type_ = "Tech"
                await sqlitedb.store_temp_event_info(chat_id=chat_id,type=type_)
                await club_event_handler.store_edited_event_values(chat_id)
                await sqlitedb.set_permissions(chat_id)
                temp_event_info = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id=chat_id)
                event_id = temp_event_info[0]
                button = []
                button.append([InlineKeyboardButton("Back",callback_data=f"EVENT-edit_event_info-{event_id}")])
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[5],
                    reply_markup = button
                )
            elif data_part[1] == "non_tech_event":
                chat_id = callback_query.message.chat.id
                type_ = "Non-Tech"
                await sqlitedb.store_temp_event_info(chat_id=chat_id,type=type_)
                await club_event_handler.initialize_storing_event_values(chat_id)
                await sqlitedb.set_permissions(chat_id)
                temp_event_info = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id=chat_id)
                event_id = temp_event_info[0]
                button = []
                button.append([InlineKeyboardButton("Back",callback_data=f"EVENT-edit_event_info-{event_id}")])
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[5],
                    reply_markup = button
                )
                
    elif data_part[3] == "up":
        if data_part[1] == "date":
            current_day = int(callback_query.data.split("-")[4])
            current_month = int(callback_query.data.split("-")[5])
            current_year = int(callback_query.data.split("-")[6])

            if data_part[2] == "day":
                current_day += 1
            elif data_part[2] == "month":
                current_month += 1
            elif data_part[2] == "year":
                current_year += 1
            else:
                return

            if current_month > 12:
                current_month = 1
                current_year += 1

            days_in_month = calendar.monthrange(current_year, current_month)[1]

            if current_day > days_in_month:
                current_day = 1
                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1

            try:
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[1],
                    reply_markup=await generate_date_picker_buttons(
                        method="EVENT",
                        current_day=current_day,
                        current_month=current_month,
                        current_year=current_year
                    )
                )
            except:
                print("")
        elif data_part[1] == "time":
            current_hour = int(callback_query.data.split("-")[4])
            current_minute = int(callback_query.data.split("-")[5])
            current_period = callback_query.data.split("-")[6]

            if data_part[2] == "hour":
                current_hour += 1
            elif data_part[2] == "minute":
                current_minute += 5
            elif data_part[2] == "period":
                current_period = "PM" if current_period == "AM" else "AM"
            else:
                return

            if current_hour > 12:
                current_hour = 1
                current_period = "PM" if current_period == "AM" else "AM"

            if current_minute >= 60:
                current_minute = 0
                current_hour += 1
                if current_hour > 12:
                    current_hour = 1
                    current_period = "PM" if current_period == "AM" else "AM"

            try:
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[2],
                    reply_markup=await generate_time_picker_buttons(
                        method="EVENT",
                        current_hour=current_hour,
                        current_minute=current_minute,
                        period=current_period
                    )
                )
            except:
                print("")

    elif data_part[3] == "down":
        if data_part[1] == "date":
            current_day = int(data_part[4])
            current_month = int(data_part[5])
            current_year = int(data_part[6])

            if data_part[2] == "day":
                current_day -= 1
            elif data_part[2] == "month":
                current_month -= 1
            elif data_part[2] == "year":
                current_year -= 1
            else:
                return

            if current_month < 1:
                current_month = 12
                current_year -= 1

            days_in_month = calendar.monthrange(current_year, current_month)[1]

            if current_day < 1:
                current_month -= 1
                if current_month < 1:
                    current_month = 12
                    current_year -= 1
                days_in_month = calendar.monthrange(current_year, current_month)[1]
                current_day = days_in_month
            try:
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[1],
                    reply_markup=await generate_date_picker_buttons(
                        method="EVENT",
                        current_day=current_day,
                        current_month=current_month,
                        current_year=current_year
                    )
                )
            except Exception as e:
                print(f"{e}")
        elif data_part[1] == "time":
            current_hour = int(data_part[4])
            current_minute = int(data_part[5])
            current_period = data_part[6]
            if data_part[2] == "hour":
                current_hour -= 1
            elif data_part[2] == "minute":
                current_minute -= 5
            elif data_part[2] == "period":
                current_period = "AM" if current_period == "PM" else "PM"
            else:
                return
            if current_hour < 1:
                current_hour = 12
            if current_minute < 0:
                current_minute = 55
                current_hour -= 1
                if current_hour < 1:
                    current_hour = 12
                    current_period = "AM" if current_period == "PM" else "PM"
            try:
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[2],
                    reply_markup=await generate_time_picker_buttons(
                        method="EVENT",
                        current_hour=current_hour,
                        current_minute=current_minute,
                        period=current_period
                    )
                )
            except Exception as e:
                print(f"{e}")


    elif data_part[1] == "submit":
        chat_id = callback_query.message.chat.id
        if data_part[2] == "date":
            current_day = data_part[3]
            current_month = data_part[4]
            current_year = data_part[5]
            try:
                await sqlitedb.store_temp_event_info(chat_id,date_time=f"{current_day}/{current_month}/{current_year}") #DD/MM/YYYY
                await callback_query.edit_message_text(
                    club_events_templates.ADD_EVENTS[2],
                    reply_markup = await generate_time_picker_buttons(method="EVENT",current_hour=12, current_minute=00,period="AM")
                )
            except Exception as e:
                print(f"Error : {e}")
        elif data_part[2] == "time":
            current_hour = data_part[3]
            current_minute = data_part[4]
            if int(current_minute) < 10:
                current_minute = f"0{current_minute}"
            if int(current_hour) < 10:
                current_hour = f"0{current_hour}"
            current_period = data_part[5]
            data = await sqlitedb.retrieve_temp_event_info_by_chat_id(chat_id) #(1767667538, None, 'hell', 1, '17/12/2024', 'iare', 1, None)
            date = data[4]
            date_time = date + f"-{current_hour}:{current_minute}:{current_period}"
            await sqlitedb.store_temp_event_info(chat_id = chat_id,date_time=date_time)
            await callback_query.edit_message_text(
                club_events_templates.ADD_EVENTS[3],
                reply_markup = tech_nontech_event_button
            )
    elif data_part[1] == "tech_event":
        chat_id = callback_query.message.chat.id
        club_id = await sqlitedb.get_club_id_by_chat_id_from_temp_events(chat_id=chat_id)
        type_ = "Tech"
        await sqlitedb.store_temp_event_info(chat_id=chat_id,type=type_)
        await club_event_handler.initialize_storing_event_values(chat_id)
        await bot.send_message(chat_id,club_events_templates.ADD_EVENTS[4])
        await callback_query.edit_message_text(
            club_events_templates.ADD_EVENTS[0],
            reply_markup = await generate_club_event_buttons(club_id=club_id)
        )
    elif data_part[1] == "non_tech_event":
        chat_id = callback_query.message.chat.id
        club_id = await sqlitedb.get_club_id_by_chat_id_from_temp_events(chat_id=chat_id)
        type_ = "Non-Tech"
        await sqlitedb.store_temp_event_info(chat_id=chat_id,type=type_)
        await club_event_handler.initialize_storing_event_values(chat_id)
        await bot.send_message(chat_id,club_events_templates.ADD_EVENTS[4])
        await callback_query.edit_message_text(
            club_events_templates.ADD_EVENTS[0],
            reply_markup = await generate_club_event_buttons(club_id=club_id)
        )
        #     if await time.is_future_date(event_report_date_str):
        #     buttons.append([InlineKeyboardButton("Event Report", callback_data=f"EVENT-event_report-{event_id}")])

        # if await time.is_future_date(proposal_form_date_str):
        #     buttons.append([InlineKeyboardButton("Proposal Form", callback_data=f"EVENT-proposal_form-{event_id}")])

        # if await time.is_future_date(flyer_and_schedule_date_str):
        #     buttons.append([InlineKeyboardButton("Flyer and Schedule", callback_data=f"EVENT-flyer_and_schedule-{event_id}")])

        # if await time.is_future_date(list_of_participants_date_str):
        #     buttons.append([InlineKeyboardButton("List of Participants", callback_data=f"EVENT-list_of_participants-{event_id}")])
    # elif data_part[1] == "event_report":
    #     chat_id = callback_query.message.chat.id
    #     event_id = data_part[2]
    #     await sqlitedb.set_permissions(chat_id=chat_id,report_upload=f"{event_id}")
    #     await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[0])
    # elif data_part[1] == "proposal_form":
    #     chat_id = callback_query.message.chat.id
    #     event_id = data_part[2]
    #     await sqlitedb.set_permissions(chat_id=chat_id,proposal_form=f"{event_id}")
    #     await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[1])
    # elif data_part[1] == "flyer_and_schedule":
    #     chat_id = callback_query.message.chat.id
    #     event_id = data_part[2]
    #     await sqlitedb.set_permissions(chat_id=chat_id,flyer=f"{event_id}")
    #     await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[2])
    # elif data_part[1] == "list_of_participants":
    #     chat_id = callback_query.message.chat.id
    #     event_id = data_part[2]
    #     await sqlitedb.set_permissions(chat_id=chat_id,list_of_participants=f"{event_id}")
    #     await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[3])
    # elif data_part[1] == "add_reporter_details":
    #     chat_id = callback_query.message.chat.id
    #     event_id = data_part[2]
    #     await sqlitedb.set_permissions(chat_id=chat_id,reporter_details=f"{event_id}")
    #     await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[6])