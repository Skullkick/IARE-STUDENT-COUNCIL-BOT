from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from templates import club_events_templates,council_templates
from handlers import club_event_handler,council_members
from utils import sqlitedb
from services import club_event_service,student_council_service
import json

back_to_initial_core_button = [InlineKeyboardButton("Back", callback_data="CORE-back_to_core_menu")]
start_buttons_student_council = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Clubs",callback_data="CLUB-back_to_initial_clubs")],
        [InlineKeyboardButton("Events",callback_data="EVENT-all_events")],
        [InlineKeyboardButton("Core Team",callback_data="CORE-initialize_core_team")],
        [InlineKeyboardButton("ENFT Team",callback_data="COUNCIL-initialize_enforcement_team")],
        [InlineKeyboardButton("View All Tasks",callback_data="COUNCIL-initialize_core_team_tasks")],
        [InlineKeyboardButton("My Profile",callback_data="COUNCIL-my_profile_student_council")]
    ]
)

add_view_core_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Add",callback_data="CORE-add_core_member")],
        [InlineKeyboardButton("View",callback_data="CORE-view_core_member")],
        [InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")]

    ]
)

add_view_enforcement_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Add",callback_data="COUNCIL-add_enforcement_member")],
        [InlineKeyboardButton("View",callback_data="COUNCIL-view_enforcement_member")],
        [InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")]
    ]
)
choose_student_council_position = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Dean", callback_data="COUNCIL-select_role-dean"),
        ],
        [
            InlineKeyboardButton("President", callback_data="COUNCIL-select_role-president"),
        ],
        [
            InlineKeyboardButton("Vice President", callback_data="COUNCIL-select_role-vice_president"),
        ],
        [
            InlineKeyboardButton("Cancel", callback_data="COUNCIL-select_role-cancel"),
        ]
    ]
)


start_core_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("TASKS",callback_data="CORE-view_tasks")]
    ]
)
async def create_enforcement_team_buttons():
    # Retrieve enforcement team chat IDs and names
    enft_team_data = await sqlitedb.get_enforcement_team_chat_ids_and_names()

    # Check if there are any enforcement team members
    if not enft_team_data:
        return False, None  # Return False if no team members are found

    # Initialize the keyboard markup for inline buttons
    buttons = []

    # Loop through each enforcement team member and create a button
    for chat_id, name in enft_team_data:
        # Create an InlineKeyboardButton for each enforcement team member
        button = InlineKeyboardButton(
            text=name,  # Button text is the member's name
            callback_data=f"ENFT-view_member-{chat_id}"  # Callback data with chat_id
        )

        # Add each button as a list item to the buttons array
        buttons.append([button])
    buttons.append([InlineKeyboardButton("Back",callback_data="COUNCIL-initialize_enforcement_team")])
    # Create the inline keyboard layout
    keyboard = InlineKeyboardMarkup(buttons)
    
    # Return True for status and the inline keyboard
    return True, keyboard
# # Function to start the user buttons.
# async def start_student_council_buttons(message):
#     """
#     This Function is used to start the user buttons with the text.
#     :param bot: Client session
#     :param message: Message of the user"""
#     await message.reply_text(council_templates,reply_markup = USER_BUTTONS)

async def generate_back_button_to_core(core_member_id):
    button = []
    button.append(InlineKeyboardButton("Back",callback_data=f"CORE-core_member_detailed_view|edit-{core_member_id}"))
    button = InlineKeyboardMarkup(inline_keyboard=[button])
    return button

async def edit_core_members_buttons(core_member_id):
    """
    Generate buttons to edit core member details. Options will be provided to edit core_name, core_member_name, 
    core_member_chat_id, and tasks. The callback query will have the format:
    CORE-edit_core_member_info-{core_member_id}-{action}.

    :param core_member_id: The ID of the core team member to edit.
    :returns: An InlineKeyboardMarkup object with buttons to edit the core member details.
    """
    # Define the buttons for editing core member details
    buttons = [
        [InlineKeyboardButton(text="Core Name", callback_data=f"CORE-edit_selected_core_member_info-{core_member_id}-core_name")],
        [InlineKeyboardButton(text="Core Member Name", callback_data=f"CORE-edit_selected_core_member_info-{core_member_id}-core_member_name")],
        [InlineKeyboardButton(text="Core Member Chat ID", callback_data=f"CORE-edit_selected_core_member_info-{core_member_id}-core_member_chat_id")],
        # [InlineKeyboardButton(text="Core Member Tasks", callback_data=f"CORE-edit_selected_core_member_info-{core_member_id}-core_tasks")],
        [InlineKeyboardButton(text="Back", callback_data=f"CORE-core_member_detailed_view|edit-{core_member_id}")]
    ]

    # Create an InlineKeyboardMarkup object
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    # Return the inline keyboard markup with buttons
    return markup

async def delete_core_task_buttons(core_member_id):
    # core_member_info = await sqlitedb.get_core_info_by_id(core_member_id)
    # if core_member_info:
    #     core_name, core_member_name, core_member_chat_id, tasks = core_member_info
    #     tasks_assigned = tasks.split("-")

    #     # Create buttons for each task, starting index from 1
    #     buttons = [
    #         [InlineKeyboardButton(
    #             text=f"{index + 1}",
    #             callback_data=f"CORE-delete_selected_task-{core_member_id}-{index+1}"
    #         )]
    #         for index, task in enumerate(tasks_assigned)
    #     ]
    #     buttons.append([InlineKeyboardButton("Back",callback_data=f"CORE-core_member_detailed_view|edit-{core_member_id}")])
    #     return buttons
    core_member_info = await sqlitedb.get_core_info_by_id(core_member_id)
    if core_member_info:
        core_name, core_member_name, core_member_chat_id, tasks = core_member_info
        tasks_assigned = json.loads(tasks)
                # Create buttons for each task, starting from index 1
        buttons = [
            [InlineKeyboardButton(
                text=f"{key}",#) {task['task']}
                callback_data=f"CORE-delete_selected_task-{core_member_id}-{key}"
            )]
            for key, task in tasks_assigned.items()
        ]
        
        # Add a "Back" button to return to the previous menu
        buttons.append([InlineKeyboardButton(
            text="Back",
            callback_data=f"CORE-core_member_detailed_view|edit-{core_member_id}"
        )])
        return buttons


async def toggle_core_task_buttons(core_member_id):
    core_member_info = await sqlitedb.get_core_info_by_id(core_member_id)
    if core_member_info:
        core_name, core_member_name, core_member_chat_id, tasks = core_member_info
        tasks_assigned = json.loads(tasks)

        # Create buttons for each task, starting from index 1
        buttons = [
            [InlineKeyboardButton(
                text=f"{key}",
                callback_data=f"CORE-toggle_selected_task-{core_member_id}-{key}"
            )]
            for key, task in tasks_assigned.items()
        ]

        # Add a "Back" button in a new row to return to the previous menu
        buttons.append([InlineKeyboardButton(
            text="Back",
            callback_data=f"CORE-start_core_member_dashboard-{core_member_id}"
        )])

        # Wrap buttons in InlineKeyboardMarkup
        buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
        return buttons



async def core_team_buttons():
    """
    This function generates the core team buttons.
    :returns: A tuple with a boolean and the button value (or an empty string).
    """
    # Fetch core member names and their IDs from the database
    core_names_ids = await sqlitedb.get_all_core_team_members()
    # Initialize the list of buttons
    buttons = []
    
    # Check if there is at least one core member
    if len(core_names_ids) >= 1:
        for core_member_id, core_name,core_member_name,core_member_chat_id,tasks in core_names_ids:
            buttons.append([InlineKeyboardButton(f"{core_name}", callback_data=f"CORE-core_member_detailed_view|edit-{core_member_id}")])
        buttons.append([InlineKeyboardButton("Back",callback_data="CORE-back_to_core_menu")])
        # Create the final keyboard markup
        final_buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        # Return True and the final button markup
        return True, final_buttons
    else:
        # Return False and an empty string if there are no core members
        return False, ''

async def generate_all_core_team_tasks():
    # Retrieve all core member chat IDs and tasks
    core_team_tasks = await sqlitedb.get_all_core_tasks_and_ids()
    if not core_team_tasks:
        return False,"There are no tasks To display",InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")]])
    # Initialize the keyboard markup for inline buttons
    buttons = []
    message_text = f"""
```
TASKS```
"""

    # Loop through each core member ID and associated tasks
    for core_member_id, tasks in core_team_tasks:

        if tasks:
        # Fetch the core member's name using the core_member_id
            core_name = await sqlitedb.get_core_member_details(core_member_id=core_member_id, core_name=True)
            core_name = core_name['core_name']
            member_name = await sqlitedb.get_core_member_details(core_member_id=core_member_id, core_member_name=True)
            member_name = member_name['core_member_name']
            

            tasks=json.loads(tasks)
            for task_id, task_info in tasks.items():
                # Add core member's name and a separator to the message text
                message_text += f"""
```{core_name} 
MEMBER : {member_name}\n
"""
                task_description = task_info.get("task")
                task_status = "Completed" if task_info.get("status", False) else "Pending"
                # Add task details to the message text
                message_text += f"Task ID {task_id}: {task_description} - Status: {task_status}\n"
                message_text += "```"
    buttons.append([InlineKeyboardButton("Back",callback_data=f"COUNCIL-back_to_start_student_council")])
    # Create the inline keyboard layout
    keyboard = InlineKeyboardMarkup(buttons)
    # Return the message text and keyboard markup
    return True,message_text, keyboard


async def council_callback_function(bot,callback_query):
    """
    This Function performs operations based on the callback data from the user for the council.
    :param bot: Client session.
    :param callback_query: callback data of the user.

    :return: This returns nothing, But performs operations.
    """
    data_part = callback_query.data.split("-")
    if data_part[1] == "initialize_enforcement_team":
        await callback_query.edit_message_text(
            council_templates.council_text[1],
            reply_markup = add_view_enforcement_button
        )
    elif data_part[1] == "initialize_core_team_tasks":
        status,text,buttons = await generate_all_core_team_tasks()
        # print(await generate_all_core_team_tasks())
        await callback_query.edit_message_text(
            text,
            reply_markup = buttons
        )
    # elif data_part[1] == "view_core_member":
    elif data_part[1] == "select_role":
        chat_id = callback_query.message.chat.id
        selected_role = data_part[2]
        field_presence_dictionary = await sqlitedb.check_student_council_field_presence(chat_id)
        if selected_role == "cancel":
            await sqlitedb.delete_student_council_member(chat_id)
            await callback_query.edit_message_text(f"Cancelled endrolling as a student council member")
        elif field_presence_dictionary[selected_role] == True:
            await callback_query.edit_message_text(f"{selected_role} role is already occupied")
        elif field_presence_dictionary[selected_role] == False:
            if selected_role == "dean":
                await sqlitedb.store_student_council_info(chat_id=chat_id,dean=True)
            elif selected_role == "president":
                await sqlitedb.store_student_council_info(chat_id=chat_id,president=True)
            elif selected_role == "vice_president":
                await sqlitedb.store_student_council_info(chat_id=chat_id,vice_president=True)
            await callback_query.edit_message_text(f"Successfully Enrolled as a Student council {selected_role} \n\n Use /admin or /start to start your panel")
    elif data_part[1] == "my_profile_student_council":
        chat_id = callback_query.message.chat.id
        # profile_text = await council_templates.student_council_member_profile_text(chat_id)
        button = []
        button.append([InlineKeyboardButton("Quit Responsibility",callback_data="COUNCIL-quit_responsibility")])
        button.append([InlineKeyboardButton("Back",callback_data="COUNCIL-back_to_start_student_council")])
        await callback_query.edit_message_text(
            await council_templates.student_council_member_profile_text(chat_id),
            reply_markup = InlineKeyboardMarkup(inline_keyboard=button)
        )
    elif data_part[1] == "back_to_start_student_council":
        await callback_query.edit_message_text(
            council_templates.council_text[2],
            reply_markup = start_buttons_student_council
        )
    elif data_part[1] == "quit_responsibility":
        chat_id = callback_query.message.chat.id
        await sqlitedb.delete_student_council_member(chat_id=chat_id)
        await callback_query.edit_message_text(
            council_templates.council_text[3]
        )
    elif data_part[1] == "add_enforcement_member":
        chat_id = callback_query.message.chat.id
        await sqlitedb.set_permissions(chat_id,enforcement_team=True)
        await callback_query.answer()
        await student_council_service.add_enforcement_team_details(bot=bot,chat_id=chat_id)
    elif data_part[1] == "view_enforcement_member":
        chat_id = callback_query.message.chat.id
        status,keyboard = await create_enforcement_team_buttons()
        text = "Select a member to view details"
        if status == False:
            text = "There are no enforcement team members"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("Back",callback_data="COUNCIL-initialize_enforcement_team")]])
        
        await callback_query.edit_message_text(
            text,
            reply_markup = keyboard
        )

async def core_team_callback_function(bot,callback_query):
    """
    This Function performs operations based on the callback data from the user for the core team.
    :param bot: Client session.
    :param callback_query: callback data of the user.

    :return: This returns nothing, But performs operations.
    """
    data_part = callback_query.data.split("-")
    if data_part[1] == "initialize_core_team":
        await callback_query.edit_message_text(
            council_templates.council_text[0],
            reply_markup = add_view_core_button
        )
    elif data_part[1] == "back_to_core_menu":
        await callback_query.answer()
        await callback_query.edit_message_text(
            council_templates.council_text[0],
            reply_markup = add_view_core_button
        )
    elif data_part[1] == "add_core_member":
        chat_id = callback_query.message.chat.id
        await callback_query.message.delete()
        await sqlitedb.set_permissions(chat_id,core_team=True)
        await student_council_service.add_core_team_details(bot,chat_id=chat_id)

    elif data_part[1] == "view_core_member":
        await callback_query.answer()
        # Get the buttons and the boolean value from the clubs_buttons function
        buttons_available, buttons_markup = await core_team_buttons()

        if buttons_available:
            # If buttons are available, use the markup
            await callback_query.edit_message_text(
                council_templates.core_team[0],
                reply_markup=buttons_markup
            )
        else:
            # If no buttons are available, provide an appropriate response
            button = InlineKeyboardMarkup(inline_keyboard=[(back_to_initial_core_button)])
            await callback_query.edit_message_text(
                council_templates.core_team[1],
                reply_markup = button
            )
    elif data_part[1] == "core_member_detailed_view|edit":
        core_member_id = callback_query.data.split("-")[2]
        # core_member_name = callback_query.data.split("-")[3]
        chat_id = callback_query.message.chat.id
        await sqlitedb.set_permissions(chat_id=chat_id)
        core_info_text = await council_templates.core_member_info(core_member_id=core_member_id)
        button = []
        button.append([InlineKeyboardButton("Edit",callback_data=f"CORE-edit_core_member_info-{core_member_id}")])
        button.append([InlineKeyboardButton("Delete",callback_data=f"CORE-delete_core_member_info-{core_member_id}")])
        button.append([InlineKeyboardButton("Tasks",callback_data=f"CORE-assign_edit_tasks-{core_member_id}")])
        button.append([InlineKeyboardButton("Back",callback_data=f"CORE-view_core_member")])
        button = InlineKeyboardMarkup(
            inline_keyboard=button
        )
        await callback_query.edit_message_text(
            core_info_text,
            reply_markup = button
        )
    elif data_part[1] == "edit_core_member_info":
        core_member_id = data_part[2]
        edit_core_info_text = await council_templates.core_member_info(core_member_id=core_member_id,edit_core=True)
        await callback_query.edit_message_text(
            edit_core_info_text,
            reply_markup = await edit_core_members_buttons(core_member_id=core_member_id)
        )
    elif data_part[1] == "assign_edit_tasks":
        core_member_id = data_part[2]
        edit_core_info_text = await council_templates.core_member_info(core_member_id=core_member_id,edit_core=True)
        buttons = [
            [InlineKeyboardButton("Assign Task", callback_data=f"CORE-assign_task-{core_member_id}")],
            [InlineKeyboardButton("Delete Task", callback_data=f"CORE-delete_task-{core_member_id}")],
            [InlineKeyboardButton("Back", callback_data=f"CORE-core_member_detailed_view|edit-{core_member_id}")]
        ]
        buttons = InlineKeyboardMarkup(buttons)
        await callback_query.edit_message_text(
            edit_core_info_text,
            reply_markup = buttons
        )
    elif data_part[1] == "delete_task":
        core_member_id = data_part[2]
        delete_task_text = await council_templates.core_member_info(core_member_id=core_member_id,edit_core=True)
        buttons = await delete_core_task_buttons(core_member_id=core_member_id)
        await callback_query.edit_message_text(
            delete_task_text,
            reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        )
    elif data_part[1] == "delete_selected_task":
        chat_id = callback_query.message.id
        core_member_id = data_part[2]
        task_id = data_part[3]
        await council_members.remove_task_and_store(callback_query=callback_query,core_member_id=core_member_id,index = int(task_id))
        await bot.send_message(chat_id,"Task has been removed successfully.")
    elif data_part[1] == "assign_task":
        chat_id = callback_query.message.chat.id
        core_member_id = data_part[2]
        core_details = await sqlitedb.get_core_info_by_id(core_member_id)
        await sqlitedb.set_permissions(chat_id=chat_id,core_team_tasks=f"{core_member_id}")
        await callback_query.edit_message_text(
            f"Please send the task you would like to assign to {core_details[0]}."
        )
    elif data_part[1] == "edit_selected_core_member_info":
        core_member_id = data_part[2]
        core_edit_action = data_part[3]
        chat_id = callback_query.message.chat.id
    
        # Set permission for the chat
        await sqlitedb.set_permissions(chat_id=chat_id, edit_core=core_edit_action)
        if sqlitedb.retrieve_temp_core_info_by_chat_id(chat_id=chat_id) is None:
            await sqlitedb.delete_temp_core_team_member_by_user_chat_id(chat_id)
    
        # Fetch the current core member information
        core_info = await sqlitedb.get_core_info_by_id(core_member_id)
    
        if len(core_info) == 4:
            stored_core_id, core_name, core_member_name, core_member_chat_id = core_info
    
        # Handle editing based on the action
        if core_edit_action == "core_name":
            # Store core info temporarily
            await sqlitedb.store_temp_core_team_info(
                chat_id=chat_id,
                core_member_id=stored_core_id,
                core_member_name=core_member_name,
                core_member_chat_id=core_member_chat_id
            )
            await bot.send_message(chat_id, "Please enter the new core name:")
            await callback_query.answer()
    
        elif core_edit_action == "core_member_name":
            # Store core info temporarily
            await sqlitedb.store_temp_core_team_info(
                chat_id=chat_id,
                core_member_id=stored_core_id,
                core_name=core_name,
                core_member_chat_id=core_member_chat_id
            )
            await bot.send_message(chat_id, "Please enter the new core member name:")
            await callback_query.answer()
    
        elif core_edit_action == "core_member_chat_id":
            # Store core info temporarily
            await sqlitedb.store_temp_core_team_info(
                chat_id=chat_id,
                core_member_id=stored_core_id,
                core_name=core_name,
                core_member_name=core_member_name
            )
            await bot.send_message(chat_id, "Please enter the new core member chat ID:")
            await callback_query.answer()
    
        else:
            await callback_query.answer("Invalid action.")
    elif data_part[1] == "delete_core_member_info":
        core_member_id = data_part[2]
        chat_id = callback_query.message.chat.id
        back_to_core_edit = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Back",callback_data=f"CORE-view_core_member")]
            ]
        )
        await callback_query.edit_message_text(
            await council_templates.delete_core_member(core_member_id=core_member_id),
            reply_markup = back_to_core_edit
        )
#     elif data_part[1] == "view_tasks":
#         chat_id = callback_query.message.chat.id
#         core_member_data = await sqlitedb.get_core_member_info_by_chat_id(chat_id)
#         tasks = json.loads(core_member_data['tasks'])
#         tasks_text = f"""
# """
    elif data_part[1] == "Toggle_task_status":
        chat_id = callback_query.message.chat.id
        core_member_data = await sqlitedb.get_core_member_info_by_chat_id(chat_id)
        core_member_id = core_member_data['core_member_index']
        text = await council_templates.core_member_info(core_member_id=core_member_id)
        buttons = await toggle_core_task_buttons(core_member_id=core_member_id)
        await callback_query.edit_message_text(
            text,
            reply_markup = buttons
        )
    elif data_part[1] == "toggle_selected_task":
        #callback_data=f"CORE-toggle_selected_task-{core_member_id}-{key}"
        core_member_id = data_part[2]
        index = data_part[3]
        await council_members.update_task_status(core_member_id=core_member_id,index=index,callback_query=callback_query)
    elif data_part[1] == "start_core_member_dashboard":
        data_part = callback_query.data.split("-")
        core_member_id = data_part[2]
        text = await council_templates.core_member_info(core_member_id=core_member_id)
        # Define the button to toggle task status
        button = [InlineKeyboardButton("Toggle Task Status", callback_data="CORE-Toggle_task_status")]
        buttons = InlineKeyboardMarkup(inline_keyboard=[button])  # Use 'buttons' for the markup
        # Edit the message text and pass the correct 'buttons' as reply_markup
        await callback_query.edit_message_text(
            text,
            reply_markup=buttons
        )


async def enforcement_team_callback_function(bot,callback_query):
    data_part = callback_query.data.split("-")
    if data_part[1] == "view_violations":
        chat_id = callback_query.message.chat.id
        await council_members.store_enft_team_violations()
        violations = await sqlitedb.retrieve_violations(status_filter='open')
        for violation in violations:
            violation_id = violation['violation_id']
            violation_text = violation['violation']
            club_name = violation['club_name']
            status = violation['status']
            text = f"""
```{club_name}VIOLATION

VIOLATION : {violation_text}
STATUS : {status}
"""
            buttons = [InlineKeyboardButton("Mark as Resolved",callback_data=f"ENFT-resolve_violation-{violation_id}")]
            buttons = InlineKeyboardMarkup(inline_keyboard=buttons)
            await bot.send_message(chat_id,text,reply_markup=buttons)
    elif data_part[1] == "resolve_violation":
        violation_id = data_part[2]
        await sqlitedb.store_violation_details(violation_id=violation_id,status='resolved')
        await callback_query.edit_message_text(
            "Violation has been marked as resolved"
        )
    elif data_part[1] == "view_member":
        chat_id = data_part[2]
        # Need to get info of this enforcement member
        enft_member_info = await sqlitedb.get_enforcement_team_member(chat_id=chat_id)
        enft_member_name = enft_member_info['name']
        enft_member_chat_id = enft_member_info['chat_id']
        enft_member_text = f"""
```
Name : {enft_member_name}

Chat id : {enft_member_chat_id}

```
"""
        buttons = []
        buttons.append([InlineKeyboardButton("Delete",callback_data=f"ENFT-delete_member-{enft_member_chat_id}")])
        buttons.append([InlineKeyboardButton("Back",callback_data=f"COUNCIL-view_enforcement_member")])
        buttons = InlineKeyboardMarkup(buttons)
        await callback_query.edit_message_text(
            enft_member_text,
            reply_markup = buttons
        )
    elif data_part[1] == "delete_member":
        enft_member_chat_id = data_part[2]
        enft_member_info = await sqlitedb.get_enforcement_team_member(chat_id=enft_member_chat_id)
        enft_member_name = enft_member_info['name']
        await sqlitedb.delete_enforcement_team_member(chat_id=enft_member_chat_id)
        buttons = []
        buttons.append([InlineKeyboardButton("Back",callback_data=f"COUNCIL-view_enforcement_member")])
        buttons = InlineKeyboardMarkup(buttons)
        await callback_query.edit_message_text(
            f"Successfully deleted enforement team member {enft_member_name}",
            reply_markup = buttons
        )
